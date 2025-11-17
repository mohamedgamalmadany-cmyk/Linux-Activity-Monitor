# Linux Activity Monitor

A lightweight activity monitoring and analytics application for Linux (Tkinter + SQLite).
This project collects shell commands, running processes, logged users and file accesses, stores events in a local SQLite database, and provides a dashboard UI with analytics.

Features
 - Dashboard with key statistic cards (events, commands, processes, files)
 - Top commands and top files tables with scroll support
 - Real-time System Resources panel (CPU, RAM, Disk, Network) using `psutil`
 - Auto-collect, manual collect, refresh, and CSV export
 - Analytics window with productivity score, top hours, work sessions, command/file patterns and insights
 - Installer script (`install.sh`) to create a virtual environment and install dependencies

Project structure (important files)
 - `main.py` — application entry point
 - `config.py` — configuration values and colors
 - `database/database_operations.py` — SQLite helpers and event storage
 - `collectors_mainpulations/` — collectors for bash history, processes, users, files
 - `statistics_export/` — statistics and CSV exporter
 - `gui/` — GUI components (header, stats cards, tables, system panel, analytics panel, etc.)
 - `system_resources_monitor.py` — psutil-based resource getters
 - `data_analyzer.py` — analytics engine producing productivity score & insights
 - `install.sh` — helper installer to setup `.venv` and install required packages
 - `requirements.txt` — package requirements (psutil, matplotlib, fpdf)

Quick start (recommended)
1. Open a terminal in the project root.
2. Make the installer executable (if not already):
```bash
chmod +x install.sh
```
3. Run the installer to create a virtual environment and install dependencies:
```bash
./install.sh
```
4. Activate the virtual environment and run the app:
```bash
source .venv/bin/activate
python3 main.py
```
Or run the installer and immediately start the app:
```bash
./install.sh --run
```

Usage notes
- The app stores events in `user_activity.db` (see `config.py`).
- Use the dashboard buttons:
  - `🔄 Collect Data` — collect data from collectors and save to database
  - `♻️ Refresh View` — refresh the UI tables and stats
  - `▶️ Start Auto` — start periodic collection (disables manual refresh while running)
  - `📤 Export CSV` — export statistics to CSV
  - `📊 Analytics` — open analytics window with productivity and insights
- The System Resources panel updates periodically (default ~2s) and shows CPU/RAM/Disk percentages and network cumulative MB.

Developer notes
- Database schema: `activity_log(id, timestamp, event_type, details)` — the analytics and collectors use this table.
- Analytics: `data_analyzer.DataAnalyzer` provides:
  - `get_productivity_score()` — 0-100 score
  - `get_most_productive_hours()`, `get_command_patterns()`, `get_file_activity_patterns()`, `get_weekly_comparison()`, `get_work_sessions()`, `get_insights()`, `generate_summary_report()`
- System monitoring: uses `psutil` via `system_resources_monitor.py`.

UI / Layout adjustments
- The dashboard now uses a scrollable content area so the UI fits smaller screens. Commands and files tables are packed compactly and contain scrollbars when needed.
- The System Resources panel was redesigned to be more compact; progress bars use a tightened style.

Dependencies
- Python 3.8+ recommended
- See `requirements.txt` — install via `pip install -r requirements.txt` (the installer does this automatically)

Troubleshooting
- If the GUI fails to open due to missing modules, ensure you activated the virtual environment created by `install.sh`.
- If `psutil` reports no values for RAM on your platform, run a quick check:
```bash
python3 -c "import system_resources_monitor as s; print(s.get_all())"
```
- If `lsof` or `w` are missing, file and user collectors may return empty results — install them via your package manager (`sudo apt install lsof procps`).

Next improvements (planned)
- Add interactive charts (matplotlib) embedded in analytics tabs
- Add search and date-range filters for tables
- Export Analytics to PDF (report generator)
- Tweak UI theming and make spacing configurable

Contributing
- Contributions welcome. Please open issues or pull requests. Keep changes modular and add tests for data processing where practical.

License
- This repository does not include an explicit license file. Please add a `LICENSE` if you intend to make the project open-source.

Contact
- For questions or to request features, open an issue in the repository.
