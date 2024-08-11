from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QApplication,
    QMessageBox,
    QProgressBar,
    QComboBox,
)
from mod_downloader import ModDownloader
from profile_manager import ProfileManager
from config import MINECRAFT_VERSIONS
from logger import logger


class InstallerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minecraft Mod Installer")
        self.setGeometry(100, 100, 300, 250)

        layout = QVBoxLayout()

        # Minecraft version selector
        self.version_label = QLabel("Select Minecraft Version:")
        layout.addWidget(self.version_label)

        self.version_selector = QComboBox()
        self.version_selector.addItems(MINECRAFT_VERSIONS)
        layout.addWidget(self.version_selector)

        self.install_button = QPushButton("Install Mods")
        self.install_button.clicked.connect(self.install_mods)
        layout.addWidget(self.install_button)

        self.status_label = QLabel("Ready to install mods.")
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.profile_manager = ProfileManager(
            MINECRAFT_VERSIONS[0]
        )  # Use the first version as default

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        QApplication.processEvents()

    def install_mods(self):
        self.progress_bar.setValue(0)
        self.status_label.setText("Downloading mods...")
        QApplication.processEvents()

        selected_version = self.version_selector.currentText()
        logger.info(
            f"Starting mod installation for Minecraft version: {selected_version}"
        )

        downloader = ModDownloader(
            minecraft_version=selected_version, progress_callback=self.update_progress
        )
        result = downloader.download_mods()

        if result is None:
            self.show_error_message(
                "Mod Download Failed",
                "Some mods could not be downloaded. They may not be compatible with this version of Minecraft yet, or there may be connectivity issues. Check the log file for details.",
            )
            self.status_label.setText("Installation failed")
            self.progress_bar.setValue(0)
            logger.error("Mod installation failed")
        else:
            self.status_label.setText("Mods downloaded successfully!")
            self.progress_bar.setValue(75)
            logger.info("Mods downloaded successfully")

            # Create the profile
            self.profile_manager = ProfileManager(selected_version)
            self.profile_manager.create_profile(result)

            self.status_label.setText("Profile created successfully!")
            self.progress_bar.setValue(100)
            logger.info("Profile created successfully")

    def show_error_message(self, title, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.exec_()
        logger.error(f"Error message shown: {title} - {message}")
