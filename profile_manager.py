import json
import os
import platform
from config import MINECRAFT_VERSION, FABRIC_VERSION

class ProfileManager:
    def __init__(self):
        self.minecraft_dir = self.get_minecraft_dir()
        self.launcher_profiles_path = os.path.join(self.minecraft_dir, 'launcher_profiles.json')

    def get_minecraft_dir(self):
        system = platform.system()
        if system == "Windows":
            return os.path.join(os.getenv('APPDATA'), '.minecraft')
        elif system == "Darwin":  # macOS
            return os.path.expanduser('~/Library/Application Support/minecraft')
        else:  # Linux and others
            return os.path.expanduser('~/.minecraft')

    def create_profile(self, mod_paths):
        # Load existing profiles
        try:
            with open(self.launcher_profiles_path, "r") as file:
                profiles = json.load(file)
        except FileNotFoundError:
            profiles = {}

        # Create a new profile
        new_profile = {
            "name": f"Fabric {MINECRAFT_VERSION}",
            "type": "custom",
            "icon": "data:image/png;base64,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",
            "lastVersionId": f"fabric-loader-{FABRIC_VERSION}-{MINECRAFT_VERSION}",
            "gameDir": self.minecraft_dir,
            "javaArgs": "-Xmx2G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M"
        }

        # Add the new profile to the existing profiles
        profiles["profiles"] = profiles.get("profiles", {})
        profiles["profiles"]["fabric-modded"] = new_profile

        # Save the updated profiles
        with open(self.launcher_profiles_path, "w") as file:
            json.dump(profiles, file, indent=4)

        print(f"Profile created at: {self.launcher_profiles_path}")