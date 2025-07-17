import sys
import os
import platform
import subprocess
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

TTL_TETHER = 65
TTL_DEFAULT = 128

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TTL Tether Switcher (Windows GUI)')
        self.setMinimumSize(400, 300)
        self.setStyleSheet('background-color: #23272e; color: #f8f8f2;')
        font = QFont('Segoe UI', 11)
        self.setFont(font)

        # Judul dan deskripsi
        self.label_title = QLabel('TTL Tether Switcher')
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet('font-size: 28px; font-weight: bold; color: #7ecfff; letter-spacing: 2px;')

        self.label_desc = QLabel('Bypass tethering detection dengan satu klik.\nAplikasi modern untuk Windows.')
        self.label_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_desc.setStyleSheet('font-size: 13px; color: #b0b0b0; margin-bottom: 10px;')

        self.label_status = QLabel('Status TTL: ...')
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_status.setStyleSheet('font-size: 18px; font-weight: bold;')

        btn_style = '''
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3a7bd5, stop:1 #00d2ff);
                color: white;
                font-size: 16px;
                padding: 12px 0;
                border: none;
                border-radius: 12px;
                margin-bottom: 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00d2ff, stop:1 #3a7bd5);
                color: #23272e;
            }
            QPushButton:pressed {
                background: #23272e;
                color: #7ecfff;
            }
        '''
        self.btn_enable = QPushButton('Aktifkan Tether (TTL=65)')
        self.btn_enable.setStyleSheet(btn_style + 'background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #43e97b, stop:1 #38f9d7);')
        self.btn_enable.clicked.connect(self.enable_ttl)

        self.btn_reset = QPushButton(f'Reset TTL Default (TTL={TTL_DEFAULT})')
        self.btn_reset.setStyleSheet(btn_style + 'background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2196f3, stop:1 #21cbf3);')
        self.btn_reset.clicked.connect(self.reset_ttl)

        # Layout
        layout = QVBoxLayout()
        layout.addSpacing(10)
        layout.addWidget(self.label_title)
        layout.addWidget(self.label_desc)
        layout.addSpacing(10)
        layout.addWidget(self.label_status)
        layout.addSpacing(10)
        layout.addWidget(self.btn_enable)
        layout.addWidget(self.btn_reset)
        layout.addStretch()
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.refresh_status()

    def enable_ttl(self):
        self.set_ttl(TTL_TETHER)
        self.refresh_status()

    def reset_ttl(self):
        self.set_ttl(TTL_DEFAULT)
        self.refresh_status()

    def refresh_status(self):
        ttl = self.get_current_ttl()
        if ttl is not None:
            if ttl == TTL_TETHER:
                self.label_status.setText('Status: Tether Mode Aktif (TTL=65)')
                self.label_status.setStyleSheet('color: #4caf50; font-size: 18px; font-weight: bold;')
            elif ttl == TTL_DEFAULT:
                self.label_status.setText(f'Status: Normal Mode (TTL=128)')
                self.label_status.setStyleSheet('color: #f8f8f2; font-size: 18px; font-weight: bold;')
            else:
                self.label_status.setText(f'Status: Custom TTL ({ttl})')
                self.label_status.setStyleSheet('color: #ffb300; font-size: 18px; font-weight: bold;')
        else:
            self.label_status.setText('Status: Tidak diketahui')
            self.label_status.setStyleSheet('color: #f44336; font-size: 18px; font-weight: bold;')

    def set_ttl(self, value):
        # Set TTL via registry (butuh admin)
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'DefaultTTL', 0, winreg.REG_DWORD, value)
            winreg.CloseKey(key)
            QMessageBox.information(self, 'Sukses', f'TTL di-set ke {value}. Restart komputer agar perubahan berlaku.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Gagal set TTL: {e}\nPastikan aplikasi dijalankan sebagai Administrator.')

    def get_current_ttl(self):
        # Cek TTL dari registry
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters', 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, 'DefaultTTL')
            winreg.CloseKey(key)
            return int(value)
        except Exception:
            return None

def main():
    if platform.system() != 'Windows':
        print('Aplikasi ini hanya untuk Windows.')
        return
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 