from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import QApplication
import sys
import config as cfg

from xmlrpc.server import SimpleXMLRPCServer

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QWidget

from functools import partial

class Screenshot(QWebEngineView):

    def capture(self, url, output_file):
        self.output_file = output_file
        self.load(QUrl(url))
        self.loadFinished.connect(self.on_loaded)
        # Create hidden view without scrollbars
        self.setAttribute(Qt.WA_DontShowOnScreen)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.page().settings().setAttribute(
            QWebEngineSettings.ShowScrollBars, False)
        self.show()

    def on_loaded(self):
        self.set_size = self.page().contentsSize().toSize()
        self.set_size.setWidth(1920)
        self.resize(self.set_size)
        QTimer.singleShot(5000, self.take_screenshot)

    def take_screenshot(self):
        self.grab().save(self.output_file, b'PNG')

app = QApplication([])

screen = Screenshot()
screen.page().profile().setHttpUserAgent(
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    )

def hello( url, output_file):
    wrapper = partial(screen.capture,  url, output_file)
    QTimer.singleShot(0, wrapper)
    
    return url

class RPCThread(QThread):
    def run(self):
        # sleep a little bit to make sure QApplication is running.
        self.sleep(1)
        print("--- starting server…")
        self.rpcserver = SimpleXMLRPCServer((cfg.host, cfg.port))
        self.rpcserver.register_function(hello)

        self.rpcserver.serve_forever()



class RPCWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.thread = RPCThread(self)
        self.thread.start()

rpcwidget = RPCWidget()
rpcwidget.show()

app.exec_()
        
