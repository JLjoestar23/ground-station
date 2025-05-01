import sys
import os
import re
import time
import numpy as np
import pandas as pd
import matplotlib as mpl
from PyQt6 import QtCore, QtWidgets, QtGui
from gsmw2 import Ui_MainWindow
import pyqtgraph as pg
import client
import random
import csv

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.connect = 0
        self.status = ""
        self.collect_data = 0
        self.log_message = ""
        self.autosave = 0
        self.autosave_text = ""
        self.output = None
        self.converted = None
        self.data_dict = {}
        self.data_point = 0
        self.idx = 0

        self.data_handler = client.DataHandler()

        self.icon_path = os.path.join(os.path.dirname(__file__), "images", "meatball.png")
        self.setWindowIcon(QtGui.QIcon(self.icon_path))
        self.setWindowTitle("Andromeda Ground Station")
        pg.setConfigOptions(antialias=True)
        pg.setConfigOptions(useOpenGL=True)

        # Header with logo and mission title
        self.header_layout = QtWidgets.QHBoxLayout()
        self.logo_label = QtWidgets.QLabel()
        self.logo_label.setPixmap(QtGui.QPixmap(self.icon_path).scaled(32, 32, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.mission_label = QtWidgets.QLabel("Mission: ORION | Status: Disconnected")
        self.mission_label.setStyleSheet("color: white; font-size: 14pt; font-weight: bold;")
        self.header_layout.addWidget(self.logo_label)
        self.header_layout.addWidget(self.mission_label)
        self.header_layout.addStretch()

        # Style for buttons
        button_style = """
        QPushButton {
            background-color: #2c2f33;
            color: #ffffff;
            border: 1px solid #7289da;
            border-radius: 6px;
            padding: 6px 12px;
            font-size: 10pt;
            font-weight: 600;
        }
        QPushButton:hover {
            background-color: #3d4148;
        }
        QPushButton:pressed {
            background-color: #5865f2;
        }
        """

        for btn in [self.ui.connect_toggle, self.ui.mission_start_toggle,
                    self.ui.save_data, self.ui.clear_data, self.ui.autosave_toggle]:
            btn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            btn.setStyleSheet(button_style)

        self.ui.log_entry.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: Consolas, monospace;
                font-size: 9pt;
                border: 1px solid #444;
            }
        """)

        # Plots setup
        plot_list = {
            "bar_alt": ["Plot1", "m"], "kf_alt": ["Plot1", "g"], "trigger_alt": ["Plot1", "b"],
            "kf_vel": ["Plot2", "b"], "Int_vel": ["Plot2", "r"], "trigger_vel": ["Plot2", "g"],
            "x_accel": ["Plot4", "y"], "y_accel": ["Plot4", "r"], "z_accel": ["Plot4", "m"],
            "x_gyr": ["Plot5", "y"], "y_gyr": ["Plot5", "r"], "z_gyr": ["Plot5", "m"],
            "x_ang": ["Plot6", "y"], "y_ang": ["Plot6", "r"], "z_ang": ["Plot6", "m"],
            "temp": ["Plot3", "y"]
        }

        for plot in [self.ui.Plot1, self.ui.Plot2, self.ui.Plot3,
                     self.ui.Plot4, self.ui.Plot5, self.ui.Plot6]:
            plot.setBackground("#1e1e1e")
            plot.showGrid(x=True, y=True, alpha=0.3)
            plot.getAxis("left").setPen(pg.mkPen(color="w"))
            plot.getAxis("bottom").setPen(pg.mkPen(color="w"))
            plot.getAxis("left").setTextPen(pg.mkPen("w"))
            plot.getAxis("bottom").setTextPen(pg.mkPen("w"))
            plot.addLegend()

        for key, (plot_name, color) in plot_list.items():
            pen = pg.mkPen(color=color, width=2)
            setattr(self.ui, key, getattr(self.ui, plot_name).plot(name=key, pen=pen))

        # Connect buttons
        self.ui.connect_toggle.clicked.connect(self.connect_to_server)
        self.ui.mission_start_toggle.clicked.connect(self.toggle_record_data)
        self.ui.autosave_toggle.clicked.connect(self.toggle_autosave)
        self.ui.save_data.clicked.connect(self.save_recorded_data)
        self.ui.clear_data.clicked.connect(self.clear_recorded_data)

        self.status_timer = QtCore.QTimer()
        self.status_timer.timeout.connect(self.update_display)
        self.status_timer.start(100)

    def connect_to_server(self):
        if self.connect == 0:
            self.status = self.data_handler.connect_websocket()
            if self.status in ["Connected", "Connected (no initial data)"]:
                self.connect = 1
                self.ui.connect_toggle.setText("Disconnect")
            self.ui.log_entry.appendPlainText(self.status)
        else:
            if self.status == "Disconnected":
                self.connect = 0
                self.ui.connect_toggle.setText("Connect")
            self.ui.log_entry.appendPlainText(self.status)

    def toggle_record_data(self):
        if self.collect_data == 0 and self.connect == 1:
            self.log_message = "Data collection started"
            self.collect_data = 1
            self.ui.mission_start_toggle.setText("Stop Recording")
        elif self.collect_data == 0 and self.connect == 0:
            self.log_message = "No connection established"
        else:
            self.log_message = "Data collection stopped"
            self.collect_data = 0
            self.ui.mission_start_toggle.setText("Start Recording")
        self.ui.log_entry.appendPlainText(self.log_message)

    def toggle_autosave(self):
        self.autosave = 1 - self.autosave
        self.ui.autosave_toggle.setText(f"Auto Save: {'On' if self.autosave else 'Off'}")

    def save_recorded_data(self):
        pass

    def clear_recorded_data(self):
        """
        Clear all recorded data from the plots.
        """
        # Iterate through all the plots and reset their data
        for data_series in ["bar_alt", "kf_alt", "trigger_alt", "kf_vel", "Int_vel", "trigger_vel",
                            "x_accel", "y_accel", "z_accel", "x_gyr", "y_gyr", "z_gyr",
                            "x_ang", "y_ang", "z_ang", "temp"]:
            plot_item = getattr(self.ui, data_series, None)
            if plot_item:
                plot_item.setData([], [])  # Clear the data for the plot

        # Reset internal data buffers
        self.x_data, self.y_data = [], []
        self.idx = 0  # Reset the index counter

    def fetch_data(self):
        self.data_point = np.random.randint(0, 100)  # Simulated data point for testing
        #if isinstance(self.data_handler.get_data(), dict):
            #self.new_dict = self.data_handler.get_data()
            #self.data_point = self.new_dict["message"]
    
    def update_plots(self):
        #self.fetch_data()
        new_data = {key: self.data_point for key in [
            "kf_alt", "trigger_alt",
            "kf_vel",
            "temp",
            "x_accel",
            "x_gyr",
            "x_ang"]}
        self.idx += 1
        max_points = 50
        
        for data_series, value in new_data.items():
            plot_item = getattr(self.ui, data_series, None)
            if plot_item:
                self.x_data, self.y_data = plot_item.getData()
                if self.x_data is None or self.y_data is None:
                    self.x_data, self.y_data = [], []
                self.x_data = list(self.x_data) + [self.idx]
                self.y_data = list(self.y_data) + [value]
                plot_item.setData(x=self.x_data[-max_points:], y=self.y_data[-max_points:])

    def update_display(self):
        # Update the display with the latest data
        self.fetch_data()
        self.ui.lat_val.setText(str(self.data_point))
        self.ui.lon_val.setText(str(self.data_point))
        self.update_plots()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec())
