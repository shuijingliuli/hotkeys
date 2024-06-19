import sys
import ctypes
import os
import psutil
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QFileDialog, QInputDialog, QSystemTrayIcon, QMenu, QAction, QDialog, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QCursor

DEFAULT_URL = "https://shenshenR0.github.io"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, relative_path)

class WallpaperApp(QMainWindow):
    def __init__(self, path, is_url=True):
        super().__init__()

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

        enum_windows_proc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_void_p)
        ctypes.windll.user32.EnumWindows(enum_windows_proc(enum_handler), 0)

        if self.hwnd_workerw:
            ctypes.windll.user32.SetParent(self.winId().__int__(), self.hwnd_workerw)

        self.setWindowFlags(self.windowFlags() | 0x00000080)  # WS_CHILD

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

        self.adjust_priority()

    def adjust_priority(self):
        pid = os.getpid()
        p = psutil.Process(pid)
        try:
            p.nice(psutil.IDLE_PRIORITY_CLASS)
        except AttributeError:
            p.nice(19)

class TrayIcon(QSystemTrayIcon):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        icon_path = resource_path("icon.png")
        self.setIcon(QIcon(icon_path))

        self.app = app

        self.menu = QMenu(parent)

        self.open_url_action = QAction("加载网址")
        self.open_url_action.triggered.connect(self.load_url)
        self.menu.addAction(self.open_url_action)

        self.open_file_action = QAction("打开文件")
        self.open_file_action.triggered.connect(self.load_file)
        self.menu.addAction(self.open_file_action)

        self.exit_action = QAction("退出")
        self.exit_action.triggered.connect(self.exit_app)
        self.menu.addAction(self.exit_action)

        self.setContextMenu(self.menu)
        self.activated.connect(self.on_click)

    def on_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            QTimer.singleShot(100, lambda: self.menu.exec_(QCursor.pos()))

    def load_url(self):
        url, ok = QInputDialog.getText(None, '加载网址作为桌面', '输入网址:')
        if ok and url:
            self.app.last_path = url
            self.app.is_last_url = True
            self.load_wallpaper(url, is_url=True)
        else:
            self.load_last_or_default()

    def load_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(None, "选择本地网页文件作为桌面", "", "HTML Files (*.html);;All Files (*)", options=options)
        if file:
            self.app.last_path = file
            self.app.is_last_url = False
            self.load_wallpaper(file, is_url=False)
        else:
            self.load_last_or_default()

    def load_wallpaper(self, path, is_url):
        if self.app.wallpaper:
            self.app.wallpaper.close()
        self.app.wallpaper = WallpaperApp(path, is_url)
        self.app.wallpaper.show()

    def load_last_or_default(self):
        if self.app.last_path:
            self.load_wallpaper(self.app.last_path, is_url=self.app.is_last_url)
        else:
            self.load_wallpaper(DEFAULT_URL, is_url=True)

    def exit_app(self):
        self.app.quit()

class MyApp(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.tray_icon = TrayIcon(self)
        self.tray_icon.show()
        self.wallpaper = None
        self.last_path = None
        self.is_last_url = True

if __name__ == '__main__':
    app = MyApp(sys.argv)
    sys.exit(app.exec_())
