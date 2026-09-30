import sys
import time
import struct
import ctypes
import ctypes.wintypes

# Windows API definitions
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
PROCESS_VM_OPERATION = 0x0008
PROCESS_QUERY_INFORMATION = 0x0400

PAGE_EXECUTE_READWRITE = 0x40
PAGE_EXECUTE_READ = 0x20
PAGE_READWRITE = 0x04

kernel32 = ctypes.windll.kernel32

# Patch signature & replacements:
# Signature around Yuna stat clamping at 0x00385650 - 0x00385680 in FFX.exe
# 45 84 8D 85 1C FF FF FF 50 6A 01 E8 C0 F9 FF FF 68 [0F 27 00 00] 6A 00 FF B5 3C FF FF FF E8 5E 3E 01 00 68 [E7 03 00 00] 6A 00 FF B5 40 FF FF FF 8B
# 0F 27 00 00 = 9999 HP clamp   -> replace with 9F 86 01 00 (99999 HP)
# E7 03 00 00 = 999 MP clamp    -> replace with 0F 27 00 00 (9999 MP)

SIG_PREFIX = bytes.fromhex("45848d851cffffff506a01e8c0f9ffff68")
SIG_FULL_ORIG = bytes.fromhex(
    "45848d851cffffff506a01e8c0f9ffff680f2700006a00ffb53cffffffe85e3e010068e70300006a00ffb540ffffff8b"
)
SIG_FULL_PATCHED = bytes.fromhex(
    "45848d851cffffff506a01e8c0f9ffff689f8601006a00ffb53cffffffe85e3e0100680f2700006a00ffb540ffffff8b"
)

def apply_runtime_patch(pid):
    print(f"[Aeon Uncap] Hooking into FFX.exe (PID: {pid})...", flush=True)
    access = PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION | PROCESS_QUERY_INFORMATION
    h_proc = kernel32.OpenProcess(access, False, pid)
    if not h_proc:
        print(f"[Aeon Uncap] ERROR: Could not open process {pid} for writing.", flush=True)
        return False

    try:
        # Determine base address or scan module memory range
        # FFX.exe typically loads around 0x00400000 (or ASLR base)
        # Search memory pages for SIG_PREFIX
        class MEMORY_BASIC_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("BaseAddress", ctypes.c_void_p),
                ("AllocationBase", ctypes.c_void_p),
                ("AllocationProtect", ctypes.c_ulong),
                ("PartitionId", ctypes.c_ushort),
                ("RegionSize", ctypes.c_size_t),
                ("State", ctypes.c_ulong),
                ("Protect", ctypes.c_ulong),
                ("Type", ctypes.c_ulong)
            ]

        mbi = MEMORY_BASIC_INFORMATION()
        address = 0
        max_address = 0x7FFFFFFF
        found_addr = None

        print("[Aeon Uncap] Scanning process memory for Aeon scaling routine...", flush=True)
        while address < max_address:
            if not kernel32.VirtualQueryEx(h_proc, ctypes.c_void_p(address), ctypes.byref(mbi), ctypes.sizeof(mbi)):
                break
            
            # Look for executable or committed code regions
            if mbi.State == 0x1000 and (mbi.Protect in (0x20, 0x40, 0x10, 0x04)):
                buffer = ctypes.create_string_buffer(mbi.RegionSize)
                bytes_read = ctypes.c_size_t()
                if kernel32.ReadProcessMemory(h_proc, ctypes.c_void_p(address), buffer, mbi.RegionSize, ctypes.byref(bytes_read)):
                    data = buffer.raw[:bytes_read.value]
                    idx = data.find(SIG_PREFIX)
                    if idx != -1:
                        target = address + idx
                        # Verify full pattern or already patched
                        sub = data[idx:idx+len(SIG_FULL_ORIG)]
                        if sub == SIG_FULL_ORIG:
                            found_addr = target
                            print(f"[Aeon Uncap] Found vanilla routine at {hex(target)}", flush=True)
                            break
                        elif sub == SIG_FULL_PATCHED:
                            print(f"[Aeon Uncap] Routine at {hex(target)} is already patched!", flush=True)
                            return True
            address += mbi.RegionSize

        if not found_addr:
            print("[Aeon Uncap] Routine signature not found in current memory pages.", flush=True)
            return False

        # Addresses for the two constants:
        # HP limit is at offset +17 (4 bytes)
        # MP limit is at offset +35 (4 bytes)
        hp_clamp_addr = found_addr + 17
        mp_clamp_addr = found_addr + 35

        old_protect = ctypes.c_ulong()
        # Ensure page is writable
        kernel32.VirtualProtectEx(h_proc, ctypes.c_void_p(found_addr), len(SIG_FULL_ORIG), PAGE_EXECUTE_READWRITE, ctypes.byref(old_protect))

        # Write 99999 (0x1869F) to HP clamp
        hp_val = struct.pack("<I", 99999)
        bytes_written = ctypes.c_size_t()
        ok_hp = kernel32.WriteProcessMemory(h_proc, ctypes.c_void_p(hp_clamp_addr), hp_val, 4, ctypes.byref(bytes_written))

        # Write 9999 (0x270F) to MP clamp
        mp_val = struct.pack("<I", 9999)
        ok_mp = kernel32.WriteProcessMemory(h_proc, ctypes.c_void_p(mp_clamp_addr), mp_val, 4, ctypes.byref(bytes_written))

        # Restore page protection
        temp = ctypes.c_ulong()
        kernel32.VirtualProtectEx(h_proc, ctypes.c_void_p(found_addr), len(SIG_FULL_ORIG), old_protect.value, ctypes.byref(temp))

        if ok_hp and ok_mp:
            print("[Aeon Uncap] SUCCESS: Aeon scaling limits patched to 99,999 HP and 9,999 MP!", flush=True)
            return True
        else:
            print("[Aeon Uncap] Failed to write patched bytes into target memory.", flush=True)
            return False

    finally:
        kernel32.CloseHandle(h_proc)

def main():
    if len(sys.argv) < 2:
        print("Usage: tracker.py <PID> [GAME_DIR]")
        sys.exit(1)

    pid = int(sys.argv[1])
    game_dir = sys.argv[2] if len(sys.argv) > 2 else ""

    print(f"[Aeon Uncap Tracker] Initialized with PID {pid}", flush=True)

    # Retry a few times in case the module is still being loaded by Steam/OS
    patched = False
    for attempt in range(15):
        if apply_runtime_patch(pid):
            patched = True
            break
        time.sleep(1.0)

    if not patched:
        print("[Aeon Uncap] Warning: Could not patch scaling limits after 15 attempts.", flush=True)

    # Keep tracker alive while game is running
    while True:
        h_check = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, pid)
        if not h_check:
            break
        exit_code = ctypes.c_ulong()
        if kernel32.GetExitCodeProcess(h_check, ctypes.byref(exit_code)):
            kernel32.CloseHandle(h_check)
            if exit_code.value != 259: # STILL_ACTIVE = 259
                break
        else:
            kernel32.CloseHandle(h_check)
            break
        time.sleep(2.0)

    print("[Aeon Uncap Tracker] Game process ended. Tracker exiting.", flush=True)

if __name__ == "__main__":
    main()
