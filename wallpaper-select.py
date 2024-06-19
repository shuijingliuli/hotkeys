import sys
import ctypes
import os
import psutil
from PyQt5.QtCore import QUrl, QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QFileDialog, QInputDialog, QSystemTrayIcon, QMenu, QAction, QDialog, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QCursor

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class WallpaperApp(QMainWindow):
    def __init__(self, path, is_url=True):
        super().__init__()

        # Get the handle of the desktop window
        hwnd_progman = ctypes.windll.user32.FindWindowW("Progman", None)
        ctypes.windll.user32.SendMessageW(hwnd_progman, 0x052C, 0, 0)

        self.hwnd_workerw = None
        def enum_handler(hwnd, lParam):
            p = ctypes.create_unicode_buffer(200)
            ctypes.windll.user32.GetClassNameW(hwnd, p, 200)
            if p.value == "WorkerW":
                hwnd_shelldll_defview = ctypes.windll.user32.FindWindowExW(hwnd, 0, "SHELLDLL_DefView", None)
                if hwnd_shelldll_defview:
                    self.hwnd_workerw = ctypes.windll.user32.FindWindowExW(0, hwnd, "WorkerW", None)
            return True

        enum_windows_proc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
        ctypes.windll.user32.EnumWindows(enum_windows_proc(enum_handler), 0)

        if self.hwnd_workerw:
            # Set the parent window
            ctypes.windll.user32.SetParent(int(self.winId()), self.hwnd_workerw)

        self.setWindowFlags(self.windowFlags() | 0x00000080)  # WS_CHILD

        # 获取屏幕的宽度和高度，并调整窗口的大小和位置以覆盖整个屏幕
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        self.setGeometry(-9, -9, screen_width + 18, screen_height)

        self.browser = QWebEngineView()

        if is_url:
            self.browser.setUrl(QUrl(path))
        else:
            local_url = QUrl.fromLocalFile(os.path.abspath(path))
            self.browser.setUrl(local_url)

        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 调整线程优先级
        self.adjust_priority()

    def adjust_priority(self):
        pid = os.getpid()
        p = psutil.Process(pid)
        p.nice(psutil.IDLE_PRIORITY_CLASS)

class TrayIcon(QSystemTrayIcon):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        icon_path = resource_path("icon.png")
        self.setIcon(QIcon(icon_path))

        self.app = app

        self.menu = QMenu(parent)

        self.open_url_action = QAction("Load from URL")
        self.open_url_action.triggered.connect(self.load_url)
        self.menu.addAction(self.open_url_action)

        self.open_file_action = QAction("Load from Local File")
        self.open_file_action.triggered.connect(self.load_file)
        self.menu.addAction(self.open_file_action)

        self.exit_action = QAction("Exit")
        self.exit_action.triggered.connect(self.exit_app)
        self.menu.addAction(self.exit_action)

        self.setContextMenu(self.menu)
        self.activated.connect(self.on_click)

    def on_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.menu.exec_(QCursor.pos())

    def load_url(self):
        url, ok = QInputDialog.getText(None, 'Input Dialog', 'Enter URL:')
        if ok and url:
            if self.app.wallpaper:
                self.app.wallpaper.close()
            self.app.wallpaper = WallpaperApp(url, is_url=True)
            self.app.wallpaper.show()
        elif ok and not url:
            pass

    def load_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(None, "Select Local HTML File", "", "HTML Files (*.html);;All Files (*)", options=options)
        if file:
            if self.app.wallpaper:
                self.app.wallpaper.close()
            self.app.wallpaper = WallpaperApp(file, is_url=False)
            self.app.wallpaper.show()
        else:
            pass

    def exit_app(self):
        self.app.quit()

class MyApp(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.tray_icon = TrayIcon(self)
        self.tray_icon.show()
        self.wallpaper = None
        self.init_wallpaper()

    def init_wallpaper(self):
        selection_dialog = SelectionDialog()
        if selection_dialog.exec_() == QDialog.Accepted:
            mode, path = selection_dialog.selected_option
            is_url = (mode == 'url')
            self.wallpaper = WallpaperApp(path, is_url)
            self.wallpaper.show()

class SelectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Source")
        self.setGeometry(100, 100, 400, 100)
        
        layout = QVBoxLayout()

        self.url_button = QPushButton("Load from URL", self)
        self.url_button.clicked.connect(self.load_url)
        layout.addWidget(self.url_button)

        self.file_button = QPushButton("Load from Local File", self)
        self.file_button.clicked.connect(self.load_file)
        layout.addWidget(self.file_button)

        self.setLayout(layout)

    def load_url(self):
        url, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter URL:')
        if ok and url:
            self.selected_option = ('url', url)
            self.accept()
        elif ok and not url:
            pass
        else:
            self.reject()

    def load_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, "Select Local HTML File", "", "HTML Files (*.html);;All Files (*)", options=options)
        if file:
            self.selected_option = ('local', file)
            self.accept()
        else:
            self.reject()

if __name__ == '__main__':
    app = MyApp(sys.argv)
    sys.exit(app.exec_())
