import sys
from PyQt5.QtWidgets import QApplication
from gui import InstallerGUI

def main():
    app = QApplication(sys.argv)
    installer = InstallerGUI()
    installer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()