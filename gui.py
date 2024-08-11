from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QApplication, QMessageBox, QProgressBar
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

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.mod_downloader = ModDownloader()
        self.profile_manager = ProfileManager()

    def install_mods(self):
        self.progress_bar.setValue(0)
        self.status_label.setText("Downloading mods...")
        QApplication.processEvents()

        downloader = ModDownloader()
        result = downloader.download_mods()

        if result is None:
            self.show_error_message("Error", 
                "Some mods may not be available for the selected Minecraft version. or there may be connectivity issues. Please try again later.")
            self.status_label.setText("Installation failed")
            self.progress_bar.setValue(0)
        else:
            self.status_label.setText("Mods downloaded successfully!")
            self.progress_bar.setValue(100)

    def show_error_message(self, title, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.exec_()