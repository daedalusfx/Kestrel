import sys
import os
import re
import time
import shutil
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta  

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QComboBox, QPlainTextEdit, QGridLayout, QGroupBox,
    QMessageBox, QSpinBox, QDateEdit, QCheckBox, QProgressBar, QFrame
)
from PyQt6.QtCore import QProcess, QDateTime, Qt, QSettings
from PyQt6.QtGui import QFont, QColor, QPalette

class KestrelLite(QWidget):
    def __init__(self):
        super().__init__()
        self.process = None
        self.is_running = False
        
        # Queue Management for Chunking
        self.chunks_queue = []
        self.total_chunks = 0
        self.current_chunk_index = 0
        self.retry_count = 0
        self.max_retries = 3
        self.current_downloaded_file = None
        
        # Ensure downloads folder exists
        self.download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(self.download_dir, exist_ok=True)

        self.init_ui()
        self.load_settings()

    def init_ui(self):
        self.setWindowTitle("Kestrel Lite - Data Downloader")
        self.setGeometry(300, 300, 700, 850)
        
        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)

        # --- Header ---
        header_label = QLabel("KESTREL")
        header_label.setObjectName("header")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)

        sub_header = QLabel("Historical Data Downloader (JSON Only)")
        sub_header.setObjectName("subheader")
        sub_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(sub_header)

        # --- Settings Section ---
        settings_frame = QFrame()
        settings_frame.setObjectName("panel")
        settings_layout = QGridLayout(settings_frame)
        settings_layout.setVerticalSpacing(15)
        settings_layout.setHorizontalSpacing(15)

        # Symbol
        settings_layout.addWidget(QLabel("Symbol:"), 0, 0)
        self.symbol_combo = QComboBox()
        self.symbol_combo.setEditable(True)
        self.symbol_combo.addItems(['eurusd', 'gbpusd', 'xauusd', 'btcusd', 'usdjpy', 'gbpjpy', 'ethusd'])
        settings_layout.addWidget(self.symbol_combo, 0, 1)

        # Timeframe
        settings_layout.addWidget(QLabel("Timeframe:"), 0, 2)
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.addItems(['tick', 'm1', 'm5', 'm15', 'm30', 'h1', 'h4', 'd1'])
        self.timeframe_combo.setCurrentText('m5')
        settings_layout.addWidget(self.timeframe_combo, 0, 3)

        # Date Range
        settings_layout.addWidget(QLabel("Start Date:"), 1, 0)
        self.from_date_edit = QDateEdit(calendarPopup=True)
        self.from_date_edit.setDate(QDateTime.currentDateTime().date().addMonths(-1))
        self.from_date_edit.setDisplayFormat("yyyy-MM-dd")
        settings_layout.addWidget(self.from_date_edit, 1, 1)

        settings_layout.addWidget(QLabel("End Date:"), 1, 2)
        self.to_date_edit = QDateEdit(calendarPopup=True)
        self.to_date_edit.setDate(QDateTime.currentDateTime().date())
        self.to_date_edit.setDisplayFormat("yyyy-MM-dd")
        settings_layout.addWidget(self.to_date_edit, 1, 3)

        # Proxy
        self.proxy_check = QCheckBox("Enable Proxychains")
        self.proxy_check.setToolTip("Prefixes the command with 'proxychains' for censored networks.")
        settings_layout.addWidget(self.proxy_check, 2, 0, 1, 2)

        main_layout.addWidget(settings_frame)

        # --- Actions Section ---
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Ready")
        main_layout.addWidget(self.progress_bar)

        self.run_button = QPushButton("Start Download")
        self.run_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_button.setObjectName("action_btn")
        self.run_button.clicked.connect(self.toggle_process)
        main_layout.addWidget(self.run_button)

        # --- Logs Section ---
        log_group = QGroupBox("Process Logs")
        log_layout = QVBoxLayout()
        self.log_output = QPlainTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText("Logs will appear here...")
        log_layout.addWidget(self.log_output)
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)

        # Apply Styles
        self.apply_stylesheet()

    def apply_stylesheet(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QLabel {
                color: #bac2de;
                font-weight: 500;
            }
            QLabel#header {
                font-size: 28px;
                font-weight: bold;
                color: #89b4fa;
                margin-bottom: 5px;
            }
            QLabel#subheader {
                font-size: 14px;
                color: #6c7086;
                margin-bottom: 10px;
            }
            QFrame#panel {
                background-color: #313244;
                border-radius: 10px;
                border: 1px solid #45475a;
            }
            QComboBox, QDateEdit, QSpinBox {
                background-color: #45475a;
                border: 1px solid #585b70;
                border-radius: 6px;
                padding: 8px;
                color: #ffffff;
                min-width: 100px;
            }
            QComboBox:focus, QDateEdit:focus {
                border: 1px solid #89b4fa;
            }
            QCheckBox {
                spacing: 8px;
                color: #a6adc8;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid #585b70;
                background-color: #45475a;
            }
            QCheckBox::indicator:checked {
                background-color: #a6e3a1;
                border-color: #a6e3a1;
            }
            QPushButton#action_btn {
                background-color: #89b4fa;
                color: #1e1e2e;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton#action_btn:hover {
                background-color: #b4befe;
            }
            QPushButton#action_btn:checked {
                background-color: #f38ba8; /* Red for Stop */
                color: #1e1e2e;
            }
            QProgressBar {
                border: 1px solid #45475a;
                border-radius: 8px;
                background-color: #313244;
                color: #ffffff;
                height: 25px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #a6e3a1;
                border-radius: 8px;
            }
            QPlainTextEdit {
                background-color: #181825;
                border: 1px solid #313244;
                border-radius: 8px;
                color: #a6adc8;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
            QGroupBox {
                border: 1px solid #45475a;
                border-radius: 8px;
                margin-top: 20px;
                font-weight: bold;
                color: #89b4fa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

    # --- Logic ---

    def generate_monthly_chunks(self, start_date, end_date):
        """Splits the date range into monthly chunks."""
        chunks = []
        current = start_date
        while current <= end_date:
            chunk_end = current + relativedelta(months=1) - timedelta(days=1)
            if chunk_end > end_date:
                chunk_end = end_date
            
            chunks.append((current.strftime("%Y-%m-%d"), chunk_end.strftime("%Y-%m-%d")))
            current = current + relativedelta(months=1)
        return chunks

    def toggle_process(self):
        if self.is_running:
            self.stop_process()
        else:
            self.start_process()

    def start_process(self):
        # UI Updates
        self.is_running = True
        self.run_button.setText("Stop Download")
        self.run_button.setChecked(True) # Styles it as 'Stop'
        self.log_output.clear()
        
        # Get Inputs
        symbol = self.symbol_combo.currentText()
        start_date = self.from_date_edit.date().toPyDate()
        end_date = self.to_date_edit.date().toPyDate()
        
        if start_date >= end_date:
            QMessageBox.warning(self, "Invalid Date", "Start date must be before End date.")
            self.stop_process()
            return

        # Prepare Queue
        self.chunks_queue = self.generate_monthly_chunks(start_date, end_date)
        self.total_chunks = len(self.chunks_queue)
        self.current_chunk_index = 0
        
        self.progress_bar.setMaximum(self.total_chunks)
        self.progress_bar.setValue(0)
        self.log(f"🚀 Starting download for {symbol.upper()} ({len(self.chunks_queue)} months)...")
        
        self.run_next_chunk()

    def stop_process(self):
        if self.process and self.process.state() == QProcess.ProcessState.Running:
            self.process.kill()
        self.is_running = False
        self.run_button.setText("Start Download")
        self.run_button.setChecked(False)
        self.progress_bar.setFormat("Stopped")
        self.log("🛑 Process stopped.")

    def run_next_chunk(self):
        if not self.is_running: return
        if self.current_chunk_index >= self.total_chunks:
            self.log("✨ All downloads completed successfully!")
            self.progress_bar.setFormat("Done")
            self.stop_process()
            return

        chunk_start, chunk_end = self.chunks_queue[self.current_chunk_index]
        self.progress_bar.setFormat(f"Downloading: {chunk_start} to {chunk_end}")
        self.log(f"📦 Processing chunk {self.current_chunk_index + 1}/{self.total_chunks}: {chunk_start} -> {chunk_end}")

        # Construct Command
        symbol = self.symbol_combo.currentText()
        tf = self.timeframe_combo.currentText()
        
        args = ["npx", "dukascopy-node",
                "-i", symbol,
                "-from", chunk_start,
                "-to", chunk_end,
                "-t", tf,
                "-f", "json",
                "-v", "true"] # Volumes included

        command = "npx"
        if self.proxy_check.isChecked():
            # Using proxychains explicitly
            command = "proxychains"
            args.insert(0, command)
            self.log("   🔒 Using Proxychains")

        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.chunk_finished)
        
        self.current_downloaded_file = None
        self.process.start(command, args[1:] if command != "npx" else args)

    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode('utf-8', errors='ignore')
        if "File saved" in data:
            match = re.search(r"File saved: (.*\.json)", data)
            if match:
                self.current_downloaded_file = match.group(1).strip()
                self.log(f"   💾 Temp file: {self.current_downloaded_file}")

    def handle_stderr(self):
        # Filter noise, only show real errors if needed
        pass

    def chunk_finished(self, exit_code, exit_status):
        if exit_code == 0 and self.current_downloaded_file and os.path.exists(self.current_downloaded_file):
            # Move file to downloads folder with a clean name
            try:
                symbol = self.symbol_combo.currentText().upper()
                tf = self.timeframe_combo.currentText()
                date_part = self.chunks_queue[self.current_chunk_index][0]
                new_filename = f"{symbol}_{tf}_{date_part}.json"
                destination = os.path.join(self.download_dir, new_filename)
                
                shutil.move(self.current_downloaded_file, destination)
                self.log(f"   ✅ Saved to: downloads/{new_filename}")
                
                self.current_chunk_index += 1
                self.progress_bar.setValue(self.current_chunk_index)
                self.retry_count = 0
                
                # Small delay to prevent API flooding/UI freeze
                time.sleep(0.5)
                self.run_next_chunk()
                
            except Exception as e:
                self.log(f"   ❌ File Move Error: {e}")
                self.handle_retry()
        else:
            self.log(f"   ⚠️ Download failed (Code: {exit_code})")
            self.handle_retry()

    def handle_retry(self):
        self.retry_count += 1
        if self.retry_count <= self.max_retries:
            self.log(f"   🔄 Retrying ({self.retry_count}/{self.max_retries})...")
            time.sleep(2)
            self.run_next_chunk()
        else:
            self.log(f"   ❌ Failed after {self.max_retries} retries. Skipping chunk.")
            self.current_chunk_index += 1
            self.retry_count = 0
            self.run_next_chunk()

    def log(self, message):
        self.log_output.appendPlainText(message)
        # Auto scroll
        cursor = self.log_output.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.log_output.setTextCursor(cursor)

    def load_settings(self):
        settings = QSettings("KestrelLite", "Configs")
        self.symbol_combo.setCurrentText(settings.value("symbol", "eurusd"))
        self.timeframe_combo.setCurrentText(settings.value("timeframe", "m5"))
        self.proxy_check.setChecked(settings.value("proxy", False, type=bool))

    def closeEvent(self, event): # type: ignore
        settings = QSettings("KestrelLite", "Configs")
        settings.setValue("symbol", self.symbol_combo.currentText())
        settings.setValue("timeframe", self.timeframe_combo.currentText())
        settings.setValue("proxy", self.proxy_check.isChecked())
        if self.process: self.process.kill()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KestrelLite()
    window.show()
    sys.exit(app.exec())