from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from mod_downloader import ModDownloader
from profile_manager import ProfileManager

class InstallerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minecraft Mod Installer")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()
        
        self.install_button = QPushButton("Install Mods")
        self.install_button.clicked.connect(self.install_mods)
        layout.addWidget(self.install_button)

        self.status_label = QLabel("Ready to install mods.")
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.mod_downloader = ModDownloader()
        self.profile_manager = ProfileManager()

    def install_mods(self):
        self.status_label.setText("Downloading mods...")
        self.install_button.setEnabled(False)
        
        mods = self.mod_downloader.download_mods()
        self.profile_manager.create_profile(mods)
        
        self.status_label.setText(f"Mods installed successfully to:\n{self.mod_downloader.download_dir}\n"
                                  f"Profile created at:\n{self.profile_manager.launcher_profiles_path}")
        self.install_button.setEnabled(True)