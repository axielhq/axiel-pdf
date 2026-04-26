"""
Axiel PDF - ponto de entrada principal.
"""
import sys

from app.bootstrap import create_application, ensure_project_imports
from ui.components.startup_dialog import StartupDialog
from ui.main_window import MainWindow


def main():
    ensure_project_imports()
    app = create_application(sys.argv)

    startup = StartupDialog()
    startup.exec()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
