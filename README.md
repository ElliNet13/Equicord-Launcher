# VencordLauncher

A Windows utility that can be used as a drop-in replacement for the standard Discord launcher. Ensures that Vencord and, optionally, OpenAsar always remain up to date, even after a Discord update. With autostart function.

## Features
- **Detects Vencord and OpenAsar installation status**
- **Automatically installs/updates Vencord and OpenAsar as needed**
- **Downloads latest VencordInstallerCli.exe if missing**
- **Branch selection (`stable`, `ptb`, `canary`) via config**
- **Autostart integration:** adds or removes itself from Windows startup (shows up in Task Manager)
- **Minimized Discord start:** launches Discord minimized if configured
- **Fully portable**

## Usage
1. Download from the releases tab.
2. Check the config.json
3. Start the exe.
4. Make sure that you disable Discord's default autostart, if you want to use the autostart feature of this application.

## Build
1. Clone the repository
2. Make sure you have Python 3.13 installed
3. `pip install -r requirements.txt`
4. Build using the build.bat
