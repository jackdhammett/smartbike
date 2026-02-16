import subprocess
import shutil

class ChromiumController:
    def __init__(self):
        self.process = None

    def launch(self, url):
        # Find chromium binary
        chromium_bin = shutil.which("brave") or shutil.which("chromium-browser")
        if not chromium_bin:
            raise RuntimeError("Chromium not found. Please install it.")

        if self.process:
            return  # Already running

        self.process = subprocess.Popen([
            chromium_bin,
            "--kiosk",
            "--disable-infobars",
            "--noerrdialogs",
            "--disable-session-crashed-bubble",
            "--disable-translate",
            url
        ])

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None
