import sys
import time
from pathlib import Path

from logging_utils import init_logfile, log_info
from config_utils import load_config
from autostart_utils import set_autostart
from vencord_ops import (
    find_discord_appdir, is_vencord_present, ensure_vencord_cli,
    update_vencord_cli, install_openasar, install_vencord, start_discord
)

# Always use the folder where the exe (or script) is located
if getattr(sys, 'frozen', False):
    BASEDIR = Path(sys.executable).parent
    EXE_PATH = Path(sys.executable)
else:
    BASEDIR = Path(__file__).parent
    EXE_PATH = Path(sys.argv[0])

LOGFILE = BASEDIR / "latest.log"
CONFIGFILE = BASEDIR / "config.json"
CLI_PATH = BASEDIR / "VencordInstallerCli.exe"

def main():
    init_logfile(LOGFILE)
    print()
    log_info("VencordChecker started.")

    branch, openasar, autostart, start_minimized = load_config(CONFIGFILE)

    set_autostart(autostart, EXE_PATH)

    discord_app_dir = find_discord_appdir()

    if is_vencord_present(discord_app_dir):
        log_info("Vencord already present. Launching Discord...")
        start_discord(discord_app_dir, start_minimized)
        print()
        sys.exit(0)
    else:
        log_info("Vencord not found. Proceeding with installation...")
        ensure_vencord_cli(CLI_PATH)
        update_vencord_cli(CLI_PATH)
        if openasar is True or (isinstance(openasar, str) and openasar.lower() == "true"):
            install_openasar(CLI_PATH, branch)
        install_vencord(CLI_PATH, branch)
        time.sleep(1)
        log_info("Launching Discord after Vencord installation...")
        start_discord(discord_app_dir, start_minimized)
        print()
        sys.exit(0)

if __name__ == "__main__":
    main()
