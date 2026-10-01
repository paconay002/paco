import sys
from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow
from views.styles import QCSS_STYLES

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(QCSS_STYLES)

    ventana = MainWindow()
    ventana.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()