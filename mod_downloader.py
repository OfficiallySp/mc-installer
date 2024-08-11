import requests
import os
import platform
import subprocess
import shutil
from config import MODRINTH_API_URL, MOD_LIST, FABRIC_INSTALLER_URL, MINECRAFT_VERSION

class ModNotFoundError(Exception):
    pass

class ModDownloader:
    def __init__(self):
        self.api_url = MODRINTH_API_URL
        self.mod_list = MOD_LIST
        self.minecraft_dir = self.get_minecraft_dir()
        self.download_dir = os.path.join(self.minecraft_dir, 'mods')

    def get_minecraft_dir(self):
        system = platform.system()
        if system == "Windows":
            return os.path.join(os.getenv('APPDATA'), '.minecraft')
        elif system == "Darwin":  # macOS
            return os.path.expanduser('~/Library/Application Support/minecraft')
        else:  # Linux and others
            return os.path.expanduser('~/.minecraft')

    def download_mods(self):
        print(f"Downloading mods for Minecraft version: {MINECRAFT_VERSION}")
        self.install_fabric()
        downloaded_mods = []
        unavailable_mods = []

        try:
            for mod_slug in self.mod_list:
                try:
                    # Get project information
                    project_url = f"{self.api_url}/project/{mod_slug}"
                    project_response = requests.get(project_url)
                    project_response.raise_for_status()
                    project_data = project_response.json()

                    # Get versions for the specific Minecraft version
                    versions_url = f"{self.api_url}/project/{mod_slug}/version?game_versions=[\"{MINECRAFT_VERSION}\"]"
                    versions_response = requests.get(versions_url)
                    versions_response.raise_for_status()
                    versions_data = versions_response.json()

                    if not versions_data:
                        unavailable_mods.append(mod_slug)
                        raise ModNotFoundError(f"No compatible version found for {mod_slug}")

                    # Get the latest version
                    latest_version = versions_data[0]

                    # Download the mod file
                    file_url = latest_version['files'][0]['url']
                    file_name = latest_version['files'][0]['filename']
                    file_path = os.path.join(self.download_dir, file_name)

                    response = requests.get(file_url)
                    response.raise_for_status()

                    os.makedirs(self.download_dir, exist_ok=True)
                    with open(file_path, 'wb') as file:
                        file.write(response.content)

                    downloaded_mods.append(file_path)
                    print(f"Downloaded: {file_name}")

                except (requests.RequestException, ModNotFoundError) as e:
                    print(f"Error downloading {mod_slug}: {str(e)}")
                    unavailable_mods.append(mod_slug)
                    raise

        except Exception:
            # Clean up downloaded mods
            self.cleanup_downloads(downloaded_mods)
            
            error_message = f"The following mods are not available for Minecraft {MINECRAFT_VERSION}: {', '.join(unavailable_mods)}"
            print(error_message)
            print("Some mods haven't been updated yet. Please check for updates or choose a different Minecraft version.")
            raise ModNotFoundError(error_message)

        return downloaded_mods

    def cleanup_downloads(self, downloaded_mods):
        for mod_path in downloaded_mods:
            try:
                os.remove(mod_path)
                print(f"Removed: {mod_path}")
            except OSError as e:
                print(f"Error removing {mod_path}: {str(e)}")
        
        # Remove the mods directory if it's empty
        if os.path.exists(self.download_dir) and not os.listdir(self.download_dir):
            shutil.rmtree(self.download_dir)
            print(f"Removed empty directory: {self.download_dir}")

    def install_fabric(self):
        installer_path = os.path.join(self.minecraft_dir, 'fabric-installer.jar')
        
        # Download Fabric installer
        response = requests.get(FABRIC_INSTALLER_URL)
        response.raise_for_status()
        with open(installer_path, 'wb') as file:
            file.write(response.content)

        # Run Fabric installer
        subprocess.run(['java', '-jar', installer_path, 'client', '-mcversion', MINECRAFT_VERSION])
        
        # Clean up
        os.remove(installer_path)
        print("Fabric installed successfully")