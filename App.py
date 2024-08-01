import os
import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QStatusBar, QFrame, QMessageBox, QLabel, QDialog, QDialogButtonBox
from PyQt5.QtWebEngineWidgets import QWebEngineView

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chirp")
        self.setGeometry(100, 100, 1024, 768)
        self.setStyleSheet("background-color: #000000; color: white;")
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Load Jost font
        self.load_fonts()

        # Set the application icon
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")))

        main_layout = QVBoxLayout()

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("QStatusBar::item { border: none; } QStatusBar { color: white; background-color: #000000; }")
        self.status_bar.mousePressEvent = self.mousePressEvent
        self.status_bar.mouseMoveEvent = self.mouseMoveEvent

        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        main_layout.addWidget(frame)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)

        button_style = """
            QPushButton {
                background-color: #1AD063;
                border-radius: 8px;
                font-size: 16px;
                color: black;
                text-align: center;
                padding: 0;
                margin: 0;
                height: 40px;
            }
            QPushButton:hover {
                background-color: #128E3C;
            }
        """

        close_button_style = """
            QPushButton {
                background-color: #FC2C6A;
                border-radius: 8px;
                font-size: 16px;
                color: black;
                text-align: center;
                padding: 0;
                margin: 0;
                height: 40px;
            }
            QPushButton:hover {
                background-color: #D4004D;
            }
        """

        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet(button_style)
        self.back_button.setFixedSize(75, 40)
        self.back_button.clicked.connect(self.go_back)
        self.status_bar.addPermanentWidget(self.back_button)

        self.info_button = QPushButton("About")
        self.info_button.setStyleSheet(button_style)
        self.info_button.setFixedSize(75, 40)
        self.info_button.clicked.connect(self.show_info_dialog)
        self.status_bar.addPermanentWidget(self.info_button)

        self.minimize_button = QPushButton("Minimize")
        self.minimize_button.setStyleSheet(button_style)
        self.minimize_button.setFixedSize(75, 40)
        self.minimize_button.clicked.connect(self.showMinimized)
        self.status_bar.addPermanentWidget(self.minimize_button)

        self.maximize_button = QPushButton("Maximize")
        self.maximize_button.setStyleSheet(button_style)
        self.maximize_button.setFixedSize(75, 40)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        self.status_bar.addPermanentWidget(self.maximize_button)

        self.close_button = QPushButton("Close")
        self.close_button.setStyleSheet(close_button_style)
        self.close_button.setFixedSize(75, 40)
        self.close_button.clicked.connect(self.close)
        self.status_bar.addPermanentWidget(self.close_button)

        self.web_view = QWebEngineView()
        frame_layout.addWidget(self.web_view)

        self.load_default_homepage()

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.show()

    def load_fonts(self):
        # Load Jost font
        jost_font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Jost-Regular.ttf")
        if not os.path.exists(jost_font_path):
            raise FileNotFoundError("Jost-Regular.ttf font file not found in the application directory.")
        jost_font_id = QFontDatabase.addApplicationFont(jost_font_path)
        if jost_font_id == -1:
            print("Failed to load Jost font")
        else:
            jost_font_family = QFontDatabase.applicationFontFamilies(jost_font_id)[0]
            jost_font = QFont(jost_font_family)
            QApplication.setFont(jost_font)
            print(f"Jost font loaded successfully: {jost_font_family}")

    def load_default_homepage(self):
        self.web_view.load(QUrl("https://beta.chirpsocial.net"))

    def go_back(self):
        self.web_view.back()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if hasattr(self, 'drag_position'):
                self.move(event.globalPos() - self.drag_position)

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.maximize_button.setText("Maximize")
        else:
            self.showMaximized()
            self.maximize_button.setText("Restore")

    def show_info_dialog(self):
        message = """
        <p style="color: white;">Chirp is an open-source alternative to Twitter.</p>
        <p><a href="https://beta.chirpsocial.net/" style="color: #1AD063;">Website/platform</a> by <a href="https://github.com/actuallyaridan" style="color: #1AD063;">ActuallyAdrian</a>, 
        webapp by NuggyNet. The desktop webapp is based off the <a href="https://github.com/NuggyNet/NuggyNet" style="color: #1AD063;">NuggyNet Source Code</a></p>
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("About Chirp")
        dialog_layout = QVBoxLayout(dialog)

        label = QLabel(message, dialog)
        label.setTextFormat(Qt.RichText)
        label.setOpenExternalLinks(True)
        label.setStyleSheet("color: white;")
        dialog_layout.addWidget(label)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok, dialog)
        button_box.accepted.connect(dialog.accept)
        button_box.setStyleSheet("""
            QPushButton {
                background-color: #1AD063;
                border-radius: 8px;
                font-size: 16px;
                color: black;
                text-align: center;
                padding: 0;
                margin: 0;
                height: 40px;
            }
            QPushButton:hover {
                background-color: #128E3C;
            }
        """)
        button_box.setCenterButtons(True)
        dialog_layout.addWidget(button_box)

        dialog.exec_()

def main():
    app = QApplication(sys.argv)
    window = BrowserWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
