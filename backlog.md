# Spira Mod Manager Project Backlog & Brainstorm Memory

This file serves as the long-term memory for tracking feature ideas, polishes, and community requests for the main application.

---

## 🖥️ Main App Backlog (Proposed)

### 1. Mod Integrity & Missing Files Validator ("Spira Health Doctor") (Proposed)
* **Goal**: Audit installed and active mods for 0-byte corrupt files, missing assets, and broken staging links.
* **Details**:
  * One-click scan comparing on-disk mod assets against manifests (`modinfo.spiramod`).
  * Non-destructive 1-click auto-repair actions (re-indexing manifests, resyncing staging).

### 2. Upgraded Safe Reset & Vanilla Baseline Verifier (Proposed)
* **Goal**: Enhance existing Safe Reset into an instant, complete stock restoration tool.
* **Details**:
  * Automatic pre-reset profile snapshot for 1-click undo.
  * Sweep loose untracked injection files from `data/mods/`, `UnX_Res/`, and `efl/`.
  * Verify stock game executable and `.vbf` integrity.

### 3. Quick-Tagging & Favorites System (Proposed)
* **Goal**: Pin favorite mods and filter by custom tags.
* **Details**: Star (★) favorite mods to keep them at the top of the mod list and filter by author/user tags (*Favorites*, *Audio*, *NSFW*, *Testing*).

### 4. Fahrenheit Integration & Manifest Editor (Proposed)
* **Goal**: Fully support advanced Fahrenheit manifest customization.
* **Details**: 
  * Visual manifest editor interface to configure priorities, dependencies (`LoadAfter`), and custom configuration option parameters.
  * Integrate custom manifest flags when custom flag options are defined/supported.

---

## 💾 Done / Completed Track
* [x] **Scrollable Settings Tab & Unified Directories Layout** (Next_Release)
* [x] **Compact Mods Tab Buttons Layout** (Next_Release)
* [x] **Expanded Game-Themed UI Palettes**: custom JSON color presets (Yuna Summoner, Rikku Thief, Al Bhed Teal, Sin Ominous, Chocobo Yellow, Zanarkand Neon) parsed and loaded automatically.
* [x] **UnX Texture Mod Auto-Specialization**: detect, wrap, and normalize loose texture files under `UnX_Res/inject/textures/`.
* [x] **Dual-Game Switching**: isolated mods/configurations between FFX and FFX-2.
* [x] **Saves & Backups Manager**: automatic location, custom labels, and backup/restores.
* [x] **Mod Creator Template Form**: multi-field mod creation wizard with folder pre-generation.
* [x] **Hover Tooltips**: custom dynamic themed tooltips on active mod cards.
* [x] **Styled Plugins Tab Grouping**: dynamic sidebar container separation with highlighted borders for plugins.
* [x] **Button Theme Colorizations**: styled standard/TTK buttons to match semantic custom themes (Action, Success, Caution, Utility) dynamically (Next_Release).
* [x] **Open Plugin Developer SDK & Extensible Runner**: support raw scripts, executables, dotted path imports, background/utility/listener categories, and a starter template generator. (Next_Release)
* [x] **Advanced Plugin Developer SDK (Phase 2)**: Dynamic schema settings UI, local socket JSON-RPC server (localhost:8692), direct memory read/write API, automated pip dependency installer, and fine-grained pub/sub events with hot-reloading. (Next_Release)
* [x] **FFX Codec String Terminator Fix**: resolved premature string cutoff when text command parameters (like colors/variables) were 0x00 (Next_Release).
* [x] **Integrated External Tools Quick-Launcher (Plugin Toolkit)**: configures and quick-launches FFX modding utilities dynamically via the Plugin Toolkit Actions card (Next_Release).
* [x] **Local Cloud Save Auto-Sync**: automatically backs up FFX/FFX-2 saves to Google Drive/OneDrive on game exit (Next_Release).
* [x] **Live Graphic Mod Asset Previewer**: parse and view texture images inside mod packages in a side panel.
* [x] **Spira Modpack Engine & Bundler (`.spirapack` / `.zip`)**: 1-click export and import of entire multi-mod collections with checklists, progress modals, and automated profile generation (Next_Release).
* [x] **Nexus Mod Update Checker**: query Nexus Mods API to cross-reference versions and display dynamic card update notification badges (Next_Release).
* [x] **Single Mod Standalone Zip Exporter**: 1-click packaging from card context menu or details panel into clean, distribution-ready archives with normalized relative paths, cover art, and metadata (Next_Release).
* [x] **Custom Font & UI Scale Accessibility Switcher (Adaptive Display Engine)**: real-time font family selection and UI scale adjustment (100% - 150%) with dynamic widget geometry, Treeview row heights, and persistent accessibility preferences (Next_Release).
* [x] **Interactive Character Dashboard Profiles & Ambient Backdrop Engine**: customized character personas (Tidus, Yuna, Auron, Rikku, Lulu, Paine, Wakka, Kimahri) coordinating color palettes, crest emblems, ambient quotes, and anchored semi-transparent character watermarks from `assets/characters/` (Next_Release).
