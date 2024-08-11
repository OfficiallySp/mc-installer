import json
import os
import platform
from config import FABRIC_VERSION


class ProfileManager:
    def __init__(self, minecraft_version):
        self.minecraft_version = minecraft_version
        self.minecraft_dir = self.get_minecraft_dir()
        self.launcher_profiles_path = os.path.join(
            self.minecraft_dir, "launcher_profiles.json"
        )

    def get_minecraft_dir(self):
        system = platform.system()
        if system == "Windows":
            return os.path.join(os.getenv("APPDATA"), ".minecraft")
        elif system == "Darwin":  # macOS
            return os.path.expanduser("~/Library/Application Support/minecraft")
        else:  # Linux and others
            return os.path.expanduser("~/.minecraft")

    def create_profile(self, mod_paths):
        # Load existing profiles
        try:
            with open(self.launcher_profiles_path, "r") as file:
                profiles = json.load(file)
        except FileNotFoundError:
            profiles = {}

        # Create a new profile
        new_profile = {
            "name": f"Optimized {self.minecraft_version}",
            "type": "custom",
            "icon": "data:image/png;base64,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",
            "lastVersionId": f"fabric-loader-{FABRIC_VERSION}-{self.minecraft_version}",
            "gameDir": self.minecraft_dir,
            "javaArgs": "-Xmx2G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M",
        }

        # Add the new profile to the existing profiles
        profiles["profiles"] = profiles.get("profiles", {})
        profiles["profiles"]["fabric-modded"] = new_profile

        # Save the updated profiles
        with open(self.launcher_profiles_path, "w") as file:
            json.dump(profiles, file, indent=4)

        print(f"Profile created at: {self.launcher_profiles_path}")
