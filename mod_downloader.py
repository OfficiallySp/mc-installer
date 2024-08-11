import requests
import os
import platform
import subprocess
import shutil
import re
import zipfile
import io
from config import MODRINTH_API_URL, MOD_LIST, FABRIC_INSTALLER_URL, FABRIC_VERSION, MINECRAFT_VERSIONS, GITHUB_API_URL, LITHIUM_REPO, GITHUB_TOKEN
from logger import logger

class ModNotFoundError(Exception):
    pass


class ModDownloader:
    def __init__(self, minecraft_version, progress_callback=None):
        self.api_url = MODRINTH_API_URL
        self.mod_list = MOD_LIST
        self.minecraft_dir = self.get_minecraft_dir()
        self.download_dir = os.path.join(self.minecraft_dir, "mods")
        self.minecraft_version = minecraft_version
        self.compatible_versions = self.get_compatible_versions(minecraft_version)
        self.progress_callback = progress_callback
        self.loader_version = FABRIC_VERSION

    def get_compatible_versions(self, version):
        for v in MINECRAFT_VERSIONS:
            if v["version"] == version:
                return [version] + v["compatible"]
        return [version]

    def get_minecraft_dir(self):
        system = platform.system()
        if system == "Windows":
            return os.path.join(os.getenv("APPDATA"), ".minecraft")
        elif system == "Darwin":  # macOS
            return os.path.expanduser("~/Library/Application Support/minecraft")
        else:  # Linux and others
            return os.path.expanduser("~/.minecraft")

    def download_mods(self):
        logger.info(f"Downloading mods for Minecraft version: {self.minecraft_version}")
        self.install_fabric()
        downloaded_mods = []
        unavailable_mods = []

        total_mods = len(self.mod_list)
        for index, mod_slug in enumerate(self.mod_list):
            try:
                logger.info(f"Downloading mod: {mod_slug}")
                
                if mod_slug == "lithium":
                    file_path = self.download_lithium()
                else:
                    file_path = self.download_from_modrinth(mod_slug)

                if file_path:
                    downloaded_mods.append(file_path)
                else:
                    unavailable_mods.append(mod_slug)

                # Update progress
                if self.progress_callback:
                    progress = (index + 1) / total_mods * 75
                    self.progress_callback(int(progress))

            except Exception as e:
                logger.error(f"Error downloading {mod_slug}: {str(e)}")
                unavailable_mods.append(mod_slug)

        if unavailable_mods:
            logger.warning("\nError: Some mods could not be downloaded.")
            logger.warning(
                f"The following mods are not available for Minecraft {self.minecraft_version}:"
            )
            for mod in unavailable_mods:
                logger.warning(f"- {mod}")

            self.cleanup_downloads(downloaded_mods)
            return None

        return downloaded_mods

    def download_from_modrinth(self, mod_slug):
        # Get project information
        project_url = f"{self.api_url}/project/{mod_slug}"
        project_response = requests.get(project_url)
        project_response.raise_for_status()
        project_data = project_response.json()

        # Get versions for the specific Minecraft version and Fabric loader
        versions_url = f'{self.api_url}/project/{mod_slug}/version?game_versions=["{self.minecraft_version}"]&loaders=["fabric"]'
        versions_response = requests.get(versions_url)
        versions_response.raise_for_status()
        versions_data = versions_response.json()

        if not versions_data:
            # If no exact match, try compatible versions
            versions_url = f'{self.api_url}/project/{mod_slug}/version?game_versions={self.compatible_versions}&loaders=["fabric"]'
            versions_response = requests.get(versions_url)
            versions_response.raise_for_status()
            versions_data = versions_response.json()

        if not versions_data:
            logger.warning(f"No compatible version found for {mod_slug}")
            return None

        # Get the latest version
        latest_version = versions_data[0]

        # Download the mod file
        file_url = latest_version["files"][0]["url"]
        file_name = latest_version["files"][0]["filename"]
        file_path = os.path.join(self.download_dir, file_name)

        response = requests.get(file_url)
        response.raise_for_status()

        os.makedirs(self.download_dir, exist_ok=True)
        with open(file_path, "wb") as file:
            file.write(response.content)

        logger.info(f"Downloaded: {file_name}")
        return file_path

    def download_lithium(self):
        # Use the specific workflow ID
        workflow_id = 920703
        runs_url = f"{GITHUB_API_URL}/repos/{LITHIUM_REPO}/actions/workflows/{workflow_id}/runs?status=success"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {GITHUB_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        runs_response = requests.get(runs_url, headers=headers)
        runs_response.raise_for_status()
        runs_data = runs_response.json()

        if not runs_data["workflow_runs"]:
            logger.error("No successful Lithium builds found")
            return None

        latest_run = runs_data["workflow_runs"][0]

        # Get the artifacts for the latest successful run
        artifacts_url = latest_run["artifacts_url"]
        artifacts_response = requests.get(artifacts_url, headers=headers)
        artifacts_response.raise_for_status()
        artifacts_data = artifacts_response.json()

        if not artifacts_data["artifacts"]:
            logger.error("No artifacts found for the latest Lithium build")
            return None

        # Find the correct artifact (assuming it's named 'build-artifacts')
        build_artifact = next((a for a in artifacts_data["artifacts"] if a["name"] == "build-artifacts"), None)
        if not build_artifact:
            logger.error("Lithium build artifact not found")
            return None

        # Download the artifact
        download_url = build_artifact["archive_download_url"]
        response = requests.get(download_url, headers=headers)
        response.raise_for_status()

        # Extract the correct JAR file from the zip
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            jar_files = [f for f in z.namelist() if f.endswith('.jar') and not f.endswith('-api.jar') and not f.endswith('-api-dev.jar')]
            if not jar_files:
                logger.error("No suitable JAR file found in the artifact")
                return None
            
            jar_file = jar_files[0]  # Assume the first suitable JAR is the one we want
            jar_content = z.read(jar_file)

        # Save the JAR file
        file_name = f"lithium-fabric-mc{self.minecraft_version}-{latest_run['head_sha'][:7]}.jar"
        file_path = os.path.join(self.download_dir, file_name)

        os.makedirs(self.download_dir, exist_ok=True)
        with open(file_path, "wb") as file:
            file.write(jar_content)

        logger.info(f"Downloaded Lithium: {file_name}")
        return file_path

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

        # Remove Fabric
        fabric_version = f"fabric-loader-{FABRIC_VERSION}-{self.minecraft_version}"
        fabric_dir = os.path.join(self.minecraft_dir, "versions", fabric_version)
        if os.path.exists(fabric_dir):
            shutil.rmtree(fabric_dir)
            logger.info(f"Removed Fabric: {fabric_dir}")

    def install_fabric(self):
        installer_path = os.path.join(self.minecraft_dir, "fabric-installer.jar")

        # Download Fabric installer
        response = requests.get(FABRIC_INSTALLER_URL)
        response.raise_for_status()
        with open(installer_path, "wb") as file:
            file.write(response.content)

        # Run Fabric installer
        subprocess.run(
            [
                "java",
                "-jar",
                installer_path,
                "client",
                "-noprofile",
                "-loader",
                self.loader_version,
                "-mcversion",
                self.minecraft_version,
            ]
        )

        # Clean up
        os.remove(installer_path)
        logger.info("Fabric installed successfully")