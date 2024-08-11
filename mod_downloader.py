import requests
import os
import platform
import subprocess
import shutil
from config import MODRINTH_API_URL, MOD_LIST, FABRIC_INSTALLER_URL
from logger import logger

class ModNotFoundError(Exception):
    pass

class ModDownloader:
    def __init__(self, minecraft_version, progress_callback=None):
        self.api_url = MODRINTH_API_URL
        self.mod_list = MOD_LIST
        self.minecraft_dir = self.get_minecraft_dir()
        self.download_dir = os.path.join(self.minecraft_dir, 'mods')
        self.minecraft_version = minecraft_version
        self.progress_callback = progress_callback

    def get_minecraft_dir(self):
        system = platform.system()
        if system == "Windows":
            return os.path.join(os.getenv('APPDATA'), '.minecraft')
        elif system == "Darwin":  # macOS
            return os.path.expanduser('~/Library/Application Support/minecraft')
        else:  # Linux and others
            return os.path.expanduser('~/.minecraft')

    def download_mods(self):
        logger.info(f"Downloading mods for Minecraft version: {self.minecraft_version}")
        self.install_fabric()
        downloaded_mods = []
        unavailable_mods = []

        total_mods = len(self.mod_list)
        for index, mod_slug in enumerate(self.mod_list):
            try:
                logger.info(f"Downloading mod: {mod_slug}")
                # Get project information
                project_url = f"{self.api_url}/project/{mod_slug}"
                project_response = requests.get(project_url)
                project_response.raise_for_status()
                project_data = project_response.json()

                # Get versions for the specific Minecraft version
                versions_url = f"{self.api_url}/project/{mod_slug}/version?game_versions=[\"{self.minecraft_version}\"]"
                versions_response = requests.get(versions_url)
                versions_response.raise_for_status()
                versions_data = versions_response.json()

                if not versions_data:
                    unavailable_mods.append(mod_slug)
                    logger.warning(f"No compatible version found for {mod_slug}")
                    continue

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
                logger.info(f"Downloaded: {file_name}")

                # Update progress
                if self.progress_callback:
                    progress = (index + 1) / total_mods * 75  # 75% of progress bar for mod downloads
                    self.progress_callback(int(progress))

            except requests.RequestException as e:
                logger.error(f"Error downloading {mod_slug}: {str(e)}")
                unavailable_mods.append(mod_slug)

        if unavailable_mods:
            logger.warning("\nError: Some mods could not be downloaded.")
            logger.warning(f"The following mods are not available for Minecraft {self.minecraft_version}:")
            for mod in unavailable_mods:
                logger.warning(f"- {mod}")

            
            self.cleanup_downloads(downloaded_mods)
            return None

        return downloaded_mods

    def cleanup_downloads(self, downloaded_mods):
        for mod_path in downloaded_mods:
            try:
                os.remove(mod_path)
                logger.info(f"Removed: {mod_path}")
            except OSError as e:
                logger.error(f"Error removing {mod_path}: {str(e)}")
        
        # Remove the mods directory if it's empty
        if os.path.exists(self.download_dir) and not os.listdir(self.download_dir):
            shutil.rmtree(self.download_dir)
            logger.info(f"Removed empty directory: {self.download_dir}")

    def install_fabric(self):
        installer_path = os.path.join(self.minecraft_dir, 'fabric-installer.jar')
        
        # Download Fabric installer
        response = requests.get(FABRIC_INSTALLER_URL)
        response.raise_for_status()
        with open(installer_path, 'wb') as file:
            file.write(response.content)

        # Run Fabric installer
        subprocess.run(['java', '-jar', installer_path, 'client', '-noprofile', '-mcversion', self.minecraft_version])
        
        # Clean up
        os.remove(installer_path)
        logger.info("Fabric installed successfully")