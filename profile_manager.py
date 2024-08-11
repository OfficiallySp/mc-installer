import json
import os
import platform
from config import FABRIC_VERSION

class ProfileManager:
    def __init__(self, minecraft_version):
        self.minecraft_version = minecraft_version
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
            "name": f"Optimized {self.minecraft_version}",
            "type": "custom",
            "icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAACXBIWXMAAAB2AAAAdgFOeyYIAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAZVQTFRFAAAAAAAAMzMzJCQkLhcXHh4eHDlHKBsbISEhIDVAIEBVVUogOzEnUkkuKRkpKSEhSyY1IlNnYC0zdDg8gWovfGgucjE5IlRrVC0wTTM9IllxfjU8gzVCIGaBgm0tdzM6gmssgm0shm8ui3Ish3EtIGaGO0FRlXwuk3ouinMvi3QukztElDpFhzlBIG6PmTxFIm+PlXouIXmdknkvIXKVIHmeqkJMmTxGH3+nIXKWoj5JrUBOIIeyy6g2yaU1wUdTnz5JwkdTt0VQsZMywqE1x6Q2IYGqr5EyII+9x0hVwUZT2Uxa2bQ3zElX0q021rA4IJfHHqPZHprN68M5IKPb6cE6H5vQ3E5c4k9d4k9eHqHYIJ3QMZvHS5e2VJWzd6K2e5yrf6W3rnd8taJqtnZ+t1pkuGRtuKZtuVxouaduucLHu5ueu6OmvK2Bva6AwVRhwrurxLa4y1Rgz69Jz7BJz9HU0c/L4dze405d5Ls45Ls56U9f7VFg7VFh7cU771Fi7+7v8sc58vLz88g6+s48/dA8/9I8xVs2zQAAAFp0Uk5TAAIFBwsREhMXGBgYGhwfHyIlLUBBQkNMT1BhYWFnbG1ubm5ucXh+f4CBhIeIip2en6GipKqts7a3t7i7xsrM0dXW293e4OHh6enq6+zt7e3y8/T19vb3+f7+g5I/5gAAAMdJREFUGNNjYAACZREGJMCtpR5qp6CCENBsa61sbvPngQtotCaXFZT48ML4isFVZU1NeW3OTFABUdvGgqam9BZDRmZ9YbCIXFtxbmadq5CVdY2jmQxQQMnPp63F1UUioiglo14bpISD192Yid+8OqepPN9eDCTCzGIgzudUUdjUkOotDRLQ84gKcpOMTMtOqtYB8bksYrMSwtS8fGvDPXVBAlIh8U2l0ZbsAg7yrIxgi41iEuMCOJG8p2oaaGPChuxhBllBOBMA5HMriNI1dsoAAAAASUVORK5CYII=",
            "lastVersionId": f"fabric-loader-{FABRIC_VERSION}-{self.minecraft_version}",
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