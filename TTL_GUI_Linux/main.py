import sys
import os
import platform
import subprocess
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

# Path skrip
SCRIPT_ENABLE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../ttl-enable.sh'))
SCRIPT_RESET = os.path.abspath(os.path.join(os.path.dirname(__file__), '../ttl-reset.sh'))

# Nilai TTL default per OS
TTL_DEFAULT = 64 if platform.system() == 'Linux' else 128

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TTL Tether Switcher (Linux GUI)')
        self.setMinimumSize(400, 260)
        self.setStyleSheet('background-color: #23272e; color: #f8f8f2;')
        font = QFont('Segoe UI', 11)
        self.setFont(font)

        # Widgets
        self.label_status = QLabel('Status TTL: ...')
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_status.setStyleSheet('font-size: 18px; font-weight: bold;')

        self.btn_enable = QPushButton('Aktifkan Tether (TTL=65)')
        self.btn_enable.setStyleSheet('background-color: #4caf50; color: white; font-size: 15px; padding: 10px;')
        self.btn_enable.clicked.connect(self.enable_ttl)

        self.btn_reset = QPushButton(f'Reset TTL Default (TTL={TTL_DEFAULT})')
        self.btn_reset.setStyleSheet('background-color: #2196f3; color: white; font-size: 15px; padding: 10px;')
        self.btn_reset.clicked.connect(self.reset_ttl)

        # Judul dan deskripsi
        self.label_title = QLabel('TTL Tether Switcher')
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet('font-size: 28px; font-weight: bold; color: #7ecfff; letter-spacing: 2px;')

        self.label_desc = QLabel('Bypass tethering detection dengan satu klik.\nAplikasi modern untuk Linux.')
        self.label_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_desc.setStyleSheet('font-size: 13px; color: #b0b0b0; margin-bottom: 10px;')

        # Update style tombol agar lebih dinamis
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
        self.btn_enable.setStyleSheet(btn_style + 'background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #43e97b, stop:1 #38f9d7);')
        self.btn_reset.setStyleSheet(btn_style + 'background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2196f3, stop:1 #21cbf3);')

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

        self.refresh_status()  # Sudah ada di __init__, pastikan status langsung tampil

    def enable_ttl(self):
        self.run_script(SCRIPT_ENABLE, 'TTL di-set ke 65 (tethering bypass aktif)')
        self.refresh_status()

    def reset_ttl(self):
        self.run_script(SCRIPT_RESET, f'TTL direset ke default ({TTL_DEFAULT})')
        self.refresh_status()

    def refresh_status(self):
        ttl = self.get_current_ttl()
        iptables_status = self.get_iptables_ttl_status()
        if ttl is not None:
            if iptables_status == 65:
                self.label_status.setText('Status: Tether Mode Aktif (TTL=65 via iptables)')
                self.label_status.setStyleSheet('color: #4caf50; font-size: 18px; font-weight: bold;')
            elif ttl == TTL_DEFAULT:
                self.label_status.setText(f'Status: Normal Mode (TTL default kernel = {TTL_DEFAULT})')
                self.label_status.setStyleSheet('color: #f8f8f2; font-size: 18px; font-weight: bold;')
            else:
                self.label_status.setText(f'Status: Custom TTL (kernel={ttl})')
                self.label_status.setStyleSheet('color: #ffb300; font-size: 18px; font-weight: bold;')
        else:
            self.label_status.setText('Status: Tidak diketahui')
            self.label_status.setStyleSheet('color: #f44336; font-size: 18px; font-weight: bold;')

    def run_script(self, script_path, success_msg):
        if not os.path.exists(script_path):
            QMessageBox.critical(self, 'Error', f'Script tidak ditemukan: {script_path}')
            return
        try:
            result = subprocess.run(['sudo', 'bash', script_path], capture_output=True, text=True)
            if result.returncode == 0:
                QMessageBox.information(self, 'Sukses', success_msg)
            else:
                QMessageBox.critical(self, 'Error', result.stderr or 'Gagal menjalankan script.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def get_current_ttl(self):
        # Cek TTL default kernel
        try:
            with open('/proc/sys/net/ipv4/ip_default_ttl') as f:
                ttl = int(f.read().strip())
            return ttl
        except Exception:
            return None

    def get_iptables_ttl_status(self):
        try:
            result = subprocess.run(['sudo', 'iptables', '-t', 'mangle', '-L', 'POSTROUTING'], capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if 'TTL set to 65' in line:
                        return 65
            return None
        except Exception:
            return None

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 