import subprocess
import sys
import webbrowser
from speaker import speak

NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

# name     : spoken name
# aliases  : words you can say after "open"
# direct   : command that is always available on Windows (tried first)
# start    : name as shown in the Start menu (found automatically, any install path)
# url      : website fallback if the app is not installed
APPS = [
    {"name": "Antigravity", "aliases": ["antigravity", "anti gravity"], "start": "Antigravity"},
    {"name": "Brave Browser", "aliases": ["brave browser", "brave"], "start": "Brave"},
    {"name": "Canva", "aliases": ["canva"], "start": "Canva", "url": "https://www.canva.com"},
    {"name": "Command Prompt", "aliases": ["command prompt", "terminal", "cmd"], "direct": "start cmd"},
    {"name": "File Explorer", "aliases": ["file explorer", "explorer"], "direct": "explorer.exe"},
    {"name": "GitHub Desktop", "aliases": ["github desktop", "github"], "start": "GitHub Desktop"},
    {"name": "Google Chrome", "aliases": ["google chrome", "chrome"], "start": "Google Chrome"},
    {"name": "IDLE", "aliases": ["python idle", "idle"], "start": "IDLE"},
    {"name": "Microsoft Edge", "aliases": ["microsoft edge", "edge"], "direct": "start msedge"},
    {"name": "Node.js", "aliases": ["node js", "nodejs", "node"], "direct": "start cmd /k node"},
    {"name": "Notepad", "aliases": ["notepad"], "direct": "notepad.exe"},
    {"name": "Recycle Bin", "aliases": ["recycle bin", "bin"], "direct": "explorer.exe shell:RecycleBinFolder"},
    {"name": "Settings", "aliases": ["settings"], "direct": "start ms-settings:"},
    {"name": "Telegram", "aliases": ["telegram"], "start": "Telegram"},
    {"name": "This PC", "aliases": ["this pc", "my computer"], "direct": "explorer.exe shell:MyComputerFolder"},
    {"name": "VS Code", "aliases": ["visual studio code", "vs code", "vscode", "code"], "start": "Visual Studio Code"},
    {"name": "WhatsApp", "aliases": ["whatsapp", "whats app"], "start": "WhatsApp"},
    {"name": "WinRAR", "aliases": ["winrar", "win rar"], "start": "WinRAR"},
    {"name": "WPS Office", "aliases": ["wps office"], "start": "WPS Office"},
    {"name": "WPS PDF", "aliases": ["wps pdf"], "start": "WPS PDF"},
]

OPEN_WORDS = ("open", "launch", "start", "run")

# longest alias first so "github desktop" wins over "github", "wps pdf" over others
ALIAS_INDEX = sorted(
    ((alias, app) for app in APPS for alias in app["aliases"]),
    key=lambda pair: len(pair[0]),
    reverse=True,
)


def _find_app(command):
    padded = f" {command} "
    for alias, app in ALIAS_INDEX:
        if f" {alias} " in padded:
            return app
    return None


def _open_from_start_menu(start_name):
    """Looks the app up in the Windows Start menu and launches it."""
    safe = start_name.replace("'", "''")
    script = (
        f"Get-StartApps | Where-Object {{ $_.Name -like '*{safe}*' }} "
        "| Select-Object -First 1 -ExpandProperty AppID"
    )
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script],
            capture_output=True, text=True, timeout=20, creationflags=NO_WINDOW,
        )
        app_id = result.stdout.strip()
        if not app_id:
            return False
        subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{app_id}"])
        return True
    except Exception as error:
        print(f"ERA: Start menu lookup failed: {error}")
        return False


def _open_app(app):
    if "direct" in app:
        subprocess.Popen(app["direct"], shell=True)
        return True

    if _open_from_start_menu(app["start"]):
        return True

    # IDLE fallback through Python itself
    if app["name"] == "IDLE":
        subprocess.Popen([sys.executable, "-m", "idlelib"])
        return True

    if "url" in app:
        webbrowser.open(app["url"])
        return True

    return False


def execute_command(command):
    command = command.lower().strip()

    # ---- Exit ----
    if any(phrase in command for phrase in ("stop era", "exit era", "shutdown era", "shut down era")):
        speak("Shutting down, Sir.")
        return "exit"

    # ---- Applications ----
    if any(word in command.split() for word in OPEN_WORDS):
        app = _find_app(command)
        if app:
            speak(f"Opening {app['name']}, Sir.")
            if not _open_app(app):
                speak(f"Sorry Sir, I couldn't find {app['name']} on this computer.")
            return

    # ---- Existing commands (unchanged) ----
    if "open youtube" in command:
        speak("Opening YouTube, Sir.")
        webbrowser.open("https://www.youtube.com")
        return

    elif "open google" in command:
        speak("Opening Google, Sir.")
        webbrowser.open("https://www.google.com")
        return

    else:
        speak("Sorry Sir, I don't know that command yet.")