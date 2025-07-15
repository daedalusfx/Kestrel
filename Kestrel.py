

import sys
import os
import json
import re
import time
from datetime import timedelta
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QComboBox, QPlainTextEdit, QGridLayout, QGroupBox,
    QMessageBox, QSpinBox, QDateEdit, QCheckBox
)
from PyQt6.QtCore import QProcess, QDateTime, Qt
from PyQt6.QtGui import QFont, QIcon, QTextCursor



# 


from PyQt6.QtWidgets import QLineEdit 
from PyQt6.QtCore import QSettings

# --- سیستم ترجمه ---
TRANSLATIONS = {
    "en": {
        "window_title": "Kestrel",
        "settings_group": "Download Settings",
        "symbol_label": "Symbol:",
        "timeframe_label": "Timeframe:",
        "mode_label": "Download Mode:",
        "mode_bars": "Latest Candles",
        "mode_date": "Date Range",
        "bars_label": "Candles Count:",
        "bars_suffix": " candles",
        "from_date_label": "From Date:",
        "to_date_label": "To Date:",
        "use_tor_label": "Use Tor Proxy (for censored regions)",
        "run_button": "Start Download & Import",
        "run_button_running": "Running...",
        "output_group": "Logs & Output",
        "invalid_date_title": "Invalid Date",
        "invalid_date_msg": "'From' date must be before 'To' date.",
        "calculating_range_msg": "Calculating time range to fetch {bars_to_fetch} candles: from {from_date} to {to_date}",
        "executing_msg": "🚀 Executing: {command}",
        "download_finished_msg": "✅ Download process finished.",
        "import_started_msg": "\n⏳ Starting import process into InfluxDB...",
        "json_file_saved_msg": "\n💡 JSON file saved at: {filepath}",
        "json_error_msg": "\n❌ Error parsing JSON file: {error}",
        "json_invalid_format_msg": "The file content might not be in a valid JSON format.",
        "json_empty_msg": "JSON file has no content to process.",
        "records_read_msg": "Read {count} records from JSON file.",
        "writing_to_db_msg": "Writing {count} points to the database...",
        "write_submitted_msg": "... Write command submitted to the client.",
        "import_success_msg": "\n� ✅ Data for symbol {symbol} successfully imported into InfluxDB.",
        "temp_file_deleted_msg": "🗑️ Temporary file {filepath} deleted.",
        "temp_file_error_msg": "⚠️ Could not delete temporary file: {error}",
        "no_data_file_msg": "\n❌ No data file found to import. Data might not be available for this time range.",
        "db_error_title": "Database Error",
        "db_error_msg": "Critical error during database import: {error}",
        "empty_file_msg": "\nDownloaded file is empty (0 bytes). Import skipped.",
        "empty_file_deleted_msg": "🗑️ Empty file {filepath} deleted.",
        "trimming_data_msg": "Downloaded {total} candles. Selecting the last {bars_to_fetch} candles...",
        "db_settings_group": "InfluxDB Settings",
        "db_url_label": "URL:",
        "db_org_label": "Organization:",
        "db_bucket_label": "Bucket:",
        "db_token_label": "Token:",
    },
    "fa": {
        "window_title": "Kestrel",
        "settings_group": "تنظیمات دانلود",
        "symbol_label": "نماد:",
        "timeframe_label": "تایم فریم:",
        "mode_label": "حالت دانلود:",
        "mode_bars": "تعداد کندل آخر",
        "mode_date": "بازه زمانی",
        "bars_label": "تعداد کندل‌ها:",
        "bars_suffix": " کندل",
        "from_date_label": "از تاریخ:",
        "to_date_label": "تا تاریخ:",
        "use_tor_label": "استفاده از پراکسی Tor (برای مناطق سانسور شده)",
        "run_button": "شروع دانلود و ورود به دیتابیس",
        "run_button_running": "در حال اجرا...",
        "output_group": "خروجی و لاگ‌ها",
        "invalid_date_title": "تاریخ نامعتبر",
        "invalid_date_msg": "تاریخ 'از' باید قبل از تاریخ 'تا' باشد.",
        "calculating_range_msg": "محاسبه بازه زمانی برای دریافت {bars_to_fetch} کندل: از {from_date} تا {to_date}",
        "executing_msg": "🚀 در حال اجرای دستور: {command}",
        "download_finished_msg": "✅ فرآیند دانلود به پایان رسید.",
        "import_started_msg": "\n⏳ شروع فرآیند ورود اطلاعات به InfluxDB...",
        "json_file_saved_msg": "\n💡 فایل JSON در مسیر زیر ذخیره شد: {filepath}",
        "json_error_msg": "\n❌ خطا در پردازش فایل JSON: {error}",
        "json_invalid_format_msg": "محتوای فایل ممکن است فرمت صحیحی نداشته باشد.",
        "json_empty_msg": "فایل JSON محتوایی برای پردازش ندارد.",
        "records_read_msg": "خوانده شدن {count} رکورد از فایل JSON.",
        "writing_to_db_msg": "در حال نوشتن {count} نقطه در دیتابیس...",
        "write_submitted_msg": "... نوشتن داده‌ها به کلاینت ارسال شد.",
        "import_success_msg": "\n💾 ✅ اطلاعات با موفقیت برای نماد {symbol} وارد InfluxDB شد.",
        "temp_file_deleted_msg": "🗑️ فایل موقت {filepath} پاک شد.",
        "temp_file_error_msg": "⚠️ نتوانست فایل موقت را پاک کند: {error}",
        "no_data_file_msg": "\n❌ فایل داده‌ای برای ورود به دیتابیس پیدا نشد. ممکن است برای این بازه زمانی داده‌ای وجود نداشته باشد.",
        "db_error_title": "خطای دیتابیس",
        "db_error_msg": "خطای بحرانی در ورود اطلاعات به دیتابیس: {error}",
        "empty_file_msg": "\nفایل دانلود شده خالی است (0 بایت). ورود اطلاعات متوقف شد.",
        "empty_file_deleted_msg": "🗑️ فایل خالی {filepath} پاک شد.",
        "trimming_data_msg": "تعداد {total} کندل دانلود شد. در حال انتخاب {bars_to_fetch} کندل آخر...",
        "db_settings_group": "تنظیمات InfluxDB",
        "db_url_label": "آدرس URL:",
        "db_org_label": "Organization نام:",
        "db_bucket_label": "نام باکت:",
        "db_token_label": "توکن دسترسی:",
    }
}

class DukascopyImporterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.current_lang = "fa"
        # self.influx_url = "http://localhost:8086"
        # self.influx_token = "BrokerLens-Secret-Token-For-Data-Analysis-Project"
        # self.influx_org = "my-org"
        # self.influx_bucket = "broker_data"
        self.process = None
        self.downloaded_filepath = None
        self.current_mode = TRANSLATIONS[self.current_lang]["mode_bars"]
        
        self.initUI()
        self.load_settings() # << این خط رو اضافه کن
        self.apply_dark_theme()
        self.retranslate_ui()
        self.update_input_mode()

    def initUI(self):
        self.setGeometry(300, 300, 850, 750)
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # --- نوار بالا: تغییر زبان ---
        top_bar_layout = QHBoxLayout()
        self.lang_button = QPushButton("Switch to English")
        self.lang_button.setObjectName("lang_button")
        self.lang_button.clicked.connect(self.toggle_language)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.lang_button)
        main_layout.addLayout(top_bar_layout)

        # --- گروه تنظیمات ---
        self.settings_groupbox = QGroupBox()
        settings_layout = QGridLayout()
        settings_layout.setSpacing(12)
        settings_layout.setContentsMargins(15, 15, 15, 15)

        self.symbol_label = QLabel()
        settings_layout.addWidget(self.symbol_label, 0, 0)
        self.symbol_combo = QComboBox()
        self.symbol_combo.addItems(['eurusd', 'gbpusd', 'btcusd', 'usdjpy', 'audusd', 'usdcad', 'usdchf'])
        self.symbol_combo.setEditable(True)
        settings_layout.addWidget(self.symbol_combo, 0, 1)

        self.timeframe_label = QLabel()
        settings_layout.addWidget(self.timeframe_label, 0, 2)
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.addItems(['tick', 'm1', 'm5', 'm15', 'm30', 'h1', 'h4', 'd1'])
        self.timeframe_combo.setCurrentText('h1')
        settings_layout.addWidget(self.timeframe_combo, 0, 3)

        self.mode_label = QLabel()
        settings_layout.addWidget(self.mode_label, 1, 0)
        self.mode_combo = QComboBox()
        self.mode_combo.currentIndexChanged.connect(self.update_input_mode)
        settings_layout.addWidget(self.mode_combo, 1, 1, 1, 3)

        self.bars_label = QLabel()
        settings_layout.addWidget(self.bars_label, 2, 0)
        self.bars_spinbox = QSpinBox()
        self.bars_spinbox.setRange(10, 100000)
        self.bars_spinbox.setSingleStep(100)
        self.bars_spinbox.setValue(1000)
        settings_layout.addWidget(self.bars_spinbox, 2, 1, 1, 3)

        self.from_date_label = QLabel()
        settings_layout.addWidget(self.from_date_label, 3, 0)
        self.from_date_edit = QDateEdit(calendarPopup=True, date=QDateTime.currentDateTime().date().addDays(-7))
        self.from_date_edit.setDisplayFormat("yyyy-MM-dd")
        settings_layout.addWidget(self.from_date_edit, 3, 1)

        self.to_date_label = QLabel()
        settings_layout.addWidget(self.to_date_label, 3, 2)
        self.to_date_edit = QDateEdit(calendarPopup=True, date=QDateTime.currentDateTime().date())
        self.to_date_edit.setDisplayFormat("yyyy-MM-dd")
        settings_layout.addWidget(self.to_date_edit, 3, 3)

        self.use_tor_checkbox = QCheckBox()
        self.use_tor_checkbox.setChecked(True)
        settings_layout.addWidget(self.use_tor_checkbox, 4, 0, 1, 4)

        self.run_button = QPushButton()
        self.run_button.setObjectName("run_button")
        self.run_button.clicked.connect(self.start_process)
        settings_layout.addWidget(self.run_button, 5, 0, 1, 4)
        
        self.settings_groupbox.setLayout(settings_layout)
        main_layout.addWidget(self.settings_groupbox)
        
        
            # --- گروه تنظیمات دیتابیس ---
        self.db_groupbox = QGroupBox() # متن عنوان در retranslate_ui تنظیم می‌شود
        db_layout = QGridLayout()
        db_layout.setSpacing(12)

        # ستون اول
        self.db_url_label = QLabel()
        db_layout.addWidget(self.db_url_label, 0, 0)
        self.db_url_edit = QLineEdit("http://localhost:8086")
        db_layout.addWidget(self.db_url_edit, 0, 1)

        self.db_org_label = QLabel()
        db_layout.addWidget(self.db_org_label, 1, 0)
        self.db_org_edit = QLineEdit("my-org")
        db_layout.addWidget(self.db_org_edit, 1, 1)

        # ستون دوم
        self.db_bucket_label = QLabel()
        db_layout.addWidget(self.db_bucket_label, 0, 2)
        self.db_bucket_edit = QLineEdit("broker_data")
        db_layout.addWidget(self.db_bucket_edit, 0, 3)

        self.db_token_label = QLabel()
        db_layout.addWidget(self.db_token_label, 1, 2)
        self.db_token_edit = QLineEdit()
        self.db_token_edit.setEchoMode(QLineEdit.EchoMode.Password)
        db_layout.addWidget(self.db_token_edit, 1, 3)

        self.db_groupbox.setLayout(db_layout)
        main_layout.addWidget(self.db_groupbox)
        

        # --- گروه خروجی ---
        self.output_groupbox = QGroupBox()
        output_layout = QVBoxLayout()
        self.output_text = QPlainTextEdit()
        self.output_text.setReadOnly(True)
        output_layout.addWidget(self.output_text)
        self.output_groupbox.setLayout(output_layout)
        main_layout.addWidget(self.output_groupbox)
        
        
        
        
    def toggle_language(self):
        self.current_lang = "en" if self.current_lang == "fa" else "fa"
        self.retranslate_ui()

    def retranslate_ui(self):
        lang = TRANSLATIONS[self.current_lang]
        self.setWindowTitle(lang["window_title"])
        self.settings_groupbox.setTitle(lang["settings_group"])
        self.symbol_label.setText(lang["symbol_label"])
        self.timeframe_label.setText(lang["timeframe_label"])
        self.mode_label.setText(lang["mode_label"])
        
        # ذخیره ایندکس فعلی قبل از پاک کردن
        current_index = self.mode_combo.currentIndex()
        self.mode_combo.clear()
        self.mode_combo.addItems([lang["mode_bars"], lang["mode_date"]])
        self.mode_combo.setCurrentIndex(current_index)

        self.bars_label.setText(lang["bars_label"])
        self.bars_spinbox.setSuffix(lang["bars_suffix"])
        self.from_date_label.setText(lang["from_date_label"])
        self.to_date_label.setText(lang["to_date_label"])
        self.use_tor_checkbox.setText(lang["use_tor_label"])
        self.run_button.setText(lang["run_button"])
        self.output_groupbox.setTitle(lang["output_group"])
        self.db_groupbox.setTitle(lang.get("db_settings_group", "InfluxDB Settings"))
        self.db_url_label.setText(lang.get("db_url_label", "URL:"))
        self.db_org_label.setText(lang.get("db_org_label", "Organization:"))
        self.db_bucket_label.setText(lang.get("db_bucket_label", "Bucket:"))
        self.db_token_label.setText(lang.get("db_token_label", "Token:"))
        
        if self.current_lang == "fa":
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            self.lang_button.setText("Switch to English")
        else:
            self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
            self.lang_button.setText("تغییر به فارسی")

    def update_input_mode(self):
        self.current_mode = self.mode_combo.currentText()
        is_bar_count_mode = (self.current_mode == TRANSLATIONS[self.current_lang]["mode_bars"])
        self.bars_label.setVisible(is_bar_count_mode)
        self.bars_spinbox.setVisible(is_bar_count_mode)
        self.from_date_label.setVisible(not is_bar_count_mode)
        self.from_date_edit.setVisible(not is_bar_count_mode)
        self.to_date_label.setVisible(not is_bar_count_mode)
        self.to_date_edit.setVisible(not is_bar_count_mode)

    def start_process(self):
        lang = TRANSLATIONS[self.current_lang]
        self.run_button.setEnabled(False)
        self.run_button.setText(lang["run_button_running"])
        self.output_text.clear()
        self.downloaded_filepath = None

        symbol = self.symbol_combo.currentText()
        timeframe = self.timeframe_combo.currentText()
        
        if self.current_mode == lang["mode_date"]:
            from_date_qdate = self.from_date_edit.date()
            to_date_qdate = self.to_date_edit.date()
            if from_date_qdate >= to_date_qdate:
                QMessageBox.warning(self, lang["invalid_date_title"], lang["invalid_date_msg"])
                self.run_button.setEnabled(True)
                self.run_button.setText(lang["run_button"])
                return
            from_date = from_date_qdate.toString("yyyy-MM-dd")
            to_date = to_date_qdate.toString("yyyy-MM-dd")
        else:
            bars_to_fetch = self.bars_spinbox.value()
            time_deltas = {'tick': timedelta(minutes=1), 'm1': timedelta(minutes=1), 'm5': timedelta(minutes=5), 'm15': timedelta(minutes=15), 'm30': timedelta(minutes=30), 'h1': timedelta(hours=1), 'h4': timedelta(hours=4), 'd1': timedelta(days=1)}
            time_delta_per_bar = time_deltas.get(timeframe, timedelta(hours=1))
            buffer_factor = 1.7
            total_seconds_to_go_back = time_delta_per_bar.total_seconds() * bars_to_fetch * buffer_factor
            to_datetime = QDateTime.currentDateTime()
            from_datetime = to_datetime.addSecs(-int(total_seconds_to_go_back))
            from_date = from_datetime.toString("yyyy-MM-dd")
            to_date = to_datetime.toString("yyyy-MM-dd")
            self.output_text.appendPlainText(lang["calculating_range_msg"].format(bars_to_fetch=bars_to_fetch, from_date=from_date, to_date=to_date))

        args = ["npx", "dukascopy-node", "-i", symbol, "-from", from_date, "-to", to_date, "-t", timeframe, "-f", "json"]
        command = ""
        if self.use_tor_checkbox.isChecked():
            command = "torsocks"
            args.insert(0, command)
            command_str = f"{command} {' '.join(args[1:])}"
        else:
            command = "npx"
            command_str = ' '.join(args)

        self.output_text.appendPlainText(lang["executing_msg"].format(command=command_str) + "\n" + "-"*60)
        
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)
        self.process.start(command, args[1:] if command == "torsocks" else args)

    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode('utf-8', errors='ignore')
        cursor = self.output_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(data)
        self.output_text.ensureCursorVisible()
        full_output = self.output_text.toPlainText()
        match = re.search(r"File saved: (.*\.json)", full_output)
        if match and not self.downloaded_filepath:
            self.downloaded_filepath = match.group(1).strip()
            self.output_text.appendPlainText(TRANSLATIONS[self.current_lang]["json_file_saved_msg"].format(filepath=self.downloaded_filepath))

    def handle_stderr(self):
        data = self.process.readAllStandardError().data().decode('utf-8', errors='ignore')
        self.output_text.appendPlainText(f"⚠️ WARNING/ERROR: {data.strip()}")

    def process_finished(self):
        lang = TRANSLATIONS[self.current_lang]
        self.output_text.appendPlainText("-" * 60 + "\n" + lang["download_finished_msg"])
        if self.downloaded_filepath and os.path.exists(self.downloaded_filepath):
            try:
                self.import_json_to_influxdb()
            except Exception as e:
                self.output_text.appendPlainText(lang["db_error_msg"].format(error=e))
                QMessageBox.critical(self, lang["db_error_title"], lang["db_error_msg"].format(error=e))
        else:
            self.output_text.appendPlainText(lang["no_data_file_msg"])
        self.run_button.setEnabled(True)
        self.run_button.setText(lang["run_button"])
        self.process = None

    def import_json_to_influxdb(self):
        lang = TRANSLATIONS[self.current_lang]
        if os.path.getsize(self.downloaded_filepath) == 0:
            self.output_text.appendPlainText(lang["empty_file_msg"])
            os.remove(self.downloaded_filepath)
            self.output_text.appendPlainText(lang["empty_file_deleted_msg"].format(filepath=self.downloaded_filepath))
            return

        self.output_text.appendPlainText(lang["import_started_msg"])
        symbol = self.symbol_combo.currentText()
        timeframe = self.timeframe_combo.currentText()
        
        try:
            with open(self.downloaded_filepath, 'r') as f:
                raw_content = f.read().strip()
                if not raw_content:
                    self.output_text.appendPlainText(lang["json_empty_msg"])
                    return
                json_to_parse = f"[{raw_content.strip(',')}]" if not raw_content.startswith('[') else raw_content
                data = json.loads(json_to_parse)
        except json.JSONDecodeError as e:
            self.output_text.appendPlainText(lang["json_error_msg"].format(error=e))
            self.output_text.appendPlainText(lang["json_invalid_format_msg"])
            return
        
        if self.current_mode == lang["mode_bars"]:
            bars_to_fetch = self.bars_spinbox.value()
            if len(data) > bars_to_fetch:
                self.output_text.appendPlainText(lang["trimming_data_msg"].format(total=len(data), bars_to_fetch=bars_to_fetch))
                data = data[-bars_to_fetch:]
            
        self.output_text.appendPlainText(lang["records_read_msg"].format(count=len(data)))
    # خواندن تنظیمات دیتابیس از رابط کاربری
    # خواندن تنظیمات دیتابیس از رابط کاربری
        influx_url = self.db_url_edit.text()
        influx_token = self.db_token_edit.text()
        influx_org = self.db_org_edit.text()
        influx_bucket = self.db_bucket_edit.text()
        with InfluxDBClient(url=influx_url, token=influx_token, org=influx_org) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            broker_name = 'Dukascopy'
            mt5_period = f"PERIOD_{timeframe.upper()}"
            points = [
                Point("price")
                .tag("broker", broker_name).tag("symbol", symbol.upper()).tag("period", mt5_period)
                .field("open", float(candle['open'])).field("high", float(candle['high']))
                .field("low", float(candle['low'])).field("close", float(candle['close']))
                .time(int(candle['timestamp']), WritePrecision.MS)
                for candle in data
            ]
            self.output_text.appendPlainText(lang["writing_to_db_msg"].format(count=len(points)))
            write_api.write(bucket=influx_bucket, org=influx_org, record=points)
            self.output_text.appendPlainText(lang["write_submitted_msg"])
        
        self.output_text.appendPlainText(lang["import_success_msg"].format(symbol=symbol.upper()))
        
        try:
            os.remove(self.downloaded_filepath)
            self.output_text.appendPlainText(lang["temp_file_deleted_msg"].format(filepath=self.downloaded_filepath))
        except OSError as e:
            self.output_text.appendPlainText(lang["temp_file_error_msg"].format(error=e))

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #dcdcdc;
                font-family: 'Tahoma';
                font-size: 10pt;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #444;
                border-radius: 8px;
                margin-top: 1em;
                padding: 1.5em;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                background-color: #3c3f41;
                border-radius: 4px;
                color: #00aaff;
            }
            QLabel {
                font-weight: bold;
                padding: 5px 0;
            }
            QComboBox, QSpinBox, QDateEdit {
                padding: 8px;
                border: 1px solid #555;
                border-radius: 4px;
                background-color: #3c3f41;
                color: #dcdcdc;
            }
            QComboBox:focus, QSpinBox:focus, QDateEdit:focus {
                border-color: #00aaff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QPushButton#run_button {
                background-color: #007acc;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 5px;
                font-size: 11pt;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton#run_button:hover {
                background-color: #008ae6;
            }
            QPushButton#run_button:pressed {
                background-color: #006bb3;
            }
            QPushButton#run_button:disabled {
                background-color: #555;
                color: #888;
            }
            QPushButton#lang_button {
                background-color: #4a4a4a;
                border: 1px solid #666;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QPushButton#lang_button:hover {
                background-color: #5a5a5a;
            }
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #4caf50;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 10px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
    def load_settings(self):
        """تنظیمات دیتابیس را از آخرین اجرا بارگذاری می‌کند."""
        settings = QSettings("KestrelApp", "DukascopyImporter")
        self.db_url_edit.setText(settings.value("db_url", "http://localhost:8086"))
        self.db_org_edit.setText(settings.value("db_org", "my-org"))
        self.db_bucket_edit.setText(settings.value("db_bucket", "broker_data"))
        self.db_token_edit.setText(settings.value("db_token", ""))

    def save_settings(self):
        """تنظیمات فعلی دیتابیس را برای اجرای بعدی ذخیره می‌کند."""
        settings = QSettings("KestrelApp", "DukascopyImporter")
        settings.setValue("db_url", self.db_url_edit.text())
        settings.setValue("db_org", self.db_org_edit.text())
        settings.setValue("db_bucket", self.db_bucket_edit.text())
        settings.setValue("db_token", self.db_token_edit.text())

    def closeEvent(self, event):
        """این متد هنگام بسته شدن برنامه اجرا شده و تنظیمات را ذخیره می‌کند."""
        self.save_settings()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DukascopyImporterApp()
    ex.show()
    sys.exit(app.exec())
