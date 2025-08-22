import os
import sys
import subprocess
import glob
import urllib.request
from pathlib import Path
from logging_utils import log_info, log_error, log_warning
import ctypes

# ----------------------------------------
# Taskbar AppUserModelID helper
# ----------------------------------------
def set_taskbar_id(app_id: str):
    """Set AppUserModelID for the current process (Windows taskbar grouping)."""
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception as e:
        log_warning(f"Failed to set AppUserModelID: {e}")

def set_child_taskbar_id(exe_path: Path, app_id: str, args=None):
    """Launch a Windows process with a custom AppUserModelID to merge taskbar icons."""
    if args is None:
        args = []

    # Use STARTUPINFO to avoid extra console windows
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    try:
        process = subprocess.Popen([str(exe_path)] + args, startupinfo=si, close_fds=True)
    except Exception as e:
        log_error(f"Failed to launch {exe_path}: {e}")
        sys.exit(1)

    # Set the AppUserModelID for this process (best-effort, some windows may already exist)
    try:
        set_taskbar_id(app_id)
    except Exception:
        pass

    return process

# ----------------------------------------
# Discord / Vencord helpers
# ----------------------------------------
def find_discord_appdir():
    localappdata = Path(os.environ.get("LOCALAPPDATA", ""))
    discord_dir = localappdata / "Discord"
    app_dirs = sorted(discord_dir.glob("app-*"), reverse=True)
    if not app_dirs:
        log_error("No Discord app-* folder found.")
        sys.exit(1)
    app_dir = app_dirs[0]
    log_info(f"Found Discord installation: {app_dir}")
    return app_dir

def is_vencord_present(app_dir):
    resources_dir = app_dir / "resources"
    found = any(Path(f).exists() for f in glob.glob(str(resources_dir / "_app.asar")))
    log_info("Vencord status: " + ("Installed" if found else "Not installed"))
    return found

def ensure_vencord_cli(cli_path):
    if cli_path.exists():
        return
    log_warning("EquilotlCli.exe not found. Downloading latest version...")
    url = "https://github.com/Equicord/Equilotl/releases/latest/download/EquilotlCli.exe"
    try:
        urllib.request.urlretrieve(url, str(cli_path))
        log_info("Downloaded EquilotlCli.exe successfully.")
    except Exception as e:
        log_error(f"Failed to download EquilotlCli.exe: {e}")
        sys.exit(1)

def update_vencord_cli(cli_path):
    log_info("Checking for updates for EquilotlCli...")
    try:
        subprocess.run([str(cli_path), "-update-self"], check=True)
    except subprocess.CalledProcessError:
        log_warning("EquilotlCli self-update failed or no update available (see above).")

def install_openasar(cli_path, branch):
    log_info(f"Installing OpenAsar for branch '{branch}'...")
    try:
        subprocess.run([str(cli_path), "-install-openasar", "-branch", branch], check=True)
    except subprocess.CalledProcessError as e:
        log_error(f"Error installing OpenAsar: {e}")
        print("Failed to install OpenAsar. Please check manually.")
        sys.exit(1)

def install_vencord(cli_path, branch):
    log_info(f"Patching Discord ({branch})...")
    try:
        subprocess.run([str(cli_path), "-install", "-branch", branch], check=True)
    except subprocess.CalledProcessError as e:
        log_error(f"Error installing Vencord: {e}")
        print("Failed to install Vencord. Please check manually.")
        sys.exit(1)

def start_discord(app_dir, minimized):
    exe_path = app_dir / "Discord.exe"
    if not exe_path.exists():
        log_error("Discord.exe not found in latest app-* folder.")
        sys.exit(1)

    app_id = "Equicord.Launcher"  # taskbar merge ID

    if minimized is True or (isinstance(minimized, str) and minimized.lower() == "true"):
        log_info("Starting Discord minimized...")
        set_child_taskbar_id(exe_path, app_id, ["--start-minimized"])
        log_info("Discord started (minimized).")
    else:
        log_info("Starting Discord...")
        set_child_taskbar_id(exe_path, app_id)
        log_info("Discord started.")
