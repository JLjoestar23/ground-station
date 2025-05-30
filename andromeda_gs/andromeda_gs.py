import sys
import os
import re
import time
import numpy as np
import pandas as pd
import matplotlib as mpl
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import pyqtSignal
from gsmw import Ui_MainWindow
import pyqtgraph as pg
import receive
from datetime import datetime


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Initialize the main window and set up UI elements.
    """
    new_data_signal = pyqtSignal()

    def __init__(self):
        # initializing GUI window
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # setting up variables
        self.connect = 0
        self.status = "Disconnected"
        self.collect_data = 0
        self.log_message = ""
        self.autosave = 0
        self.autosave_text = ""
        
        

        # setting icons
        self.icon_path = os.path.join(
            os.path.dirname(__file__), "images", "meatball.png"
        )
        self.setWindowIcon(QtGui.QIcon(self.icon_path))

        # setting window name
        self.setWindowTitle("Andromeda Ground Station")
        pg.setConfigOptions(antialias=True)
        
        # initializing plots and relevant data structures
        self.setup_plots()
        self.initialize_data_structures()

        # button color changes when hovering!
        self.ui.connect_toggle.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.ui.connect_toggle.setStyleSheet(
            """
            QPushButton {
                background-color: rgb(100,100,100);
                border-radius: 5px;
                padding: 1px;
                color: white;
                font-size: 8 px;
            }

            QPushButton:hover {
                background-color: rgb(150,150,150);
            }
            """
        )

        self.ui.mission_start_toggle.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.ui.mission_start_toggle.setStyleSheet(
            """
            QPushButton {
                background-color: rgb(100,100,100);
                border-radius: 5px;
                padding: 1px;
                color: white;
                font-size: 8 px;
            }
            
            QPushButton:hover {
                background-color: rgb(150,150,150);
            }
            """
        )

        self.ui.save_data.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.ui.save_data.setStyleSheet(
            """
            QPushButton {
                background-color: rgb(100,100,100);
                border-radius: 5px;
                padding: 1px;
                color: white;
                font-size: 8 px;
            }
            
            QPushButton:hover {
                background-color: rgb(150,150,150);
            }
            """
        )

        self.ui.clear_data.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.ui.clear_data.setStyleSheet(
            """
            QPushButton {
                background-color: rgb(100,100,100);
                border-radius: 5px;
                padding: 1px;
                color: white;
                font-size: 8 px;
            }
            
            QPushButton:hover {
                background-color: rgb(150,150,150);
            }
            """
        )

        self.ui.autosave_toggle.setCursor(
            QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        )
        self.ui.autosave_toggle.setStyleSheet(
            """
            QPushButton {
                background-color: rgb(100,100,100);
                border-radius: 5px;
                padding: 1px;
                color: white;
                font-size: 8 px;
            }
            
            QPushButton:hover {
                background-color: rgb(150,150,150);
            }
            """
        )

        # once button is clicked...
        self.ui.connect_toggle.clicked.connect(self.connect_toggle)
        self.ui.mission_start_toggle.clicked.connect(self.toggle_record_data)
        self.ui.save_data.clicked.connect(self.save_recorded_data)
        self.ui.autosave_toggle.clicked.connect(self.toggle_autosave)
        self.ui.clear_data.clicked.connect(self.clear_recorded_data)

        # Initializing timer object
        self.update_timer = QtCore.QTimer(self)
        self.update_timer.timeout.connect(self.fetch_data) # Check for data every 100 milliseconds
        self.update_timer.start(50) # Check every 10 milliseconds 
        self.new_data_signal.connect(self.main_loop) # Connect the signal to the main loop

    # general functions
    def main_loop(self): # need to figure out the exact architecture of this function
        # only fetch data if connected
        #if self.connect == 1:
        #    self.fetch_data()
        
        # update the plots and display elements
        self.update_display()

        # autosave data to CSV file if autosave is enabled every 250 data points
        # clears the recorded data after saving
        if self.autosave == 1 and len(self.recorded_data) > 250:
            self.save_recorded_data()
            self.recorded_data = pd.DataFrame(columns=[
                'time', 'Accel_X', 'Accel_Y', 'Accel_Z', 
                'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Temp',
                'Euler_X', 'Euler_Y', 'Euler_Z', 'Baro_Alt',
                'Longitude', 'Latitude', 'GPS_Alt', 'Phase',
                'Continuity', 'Voltage', 'Link_Strength',
                'KF_X', 'KF_Y', 'KF_Z', 'KF_VX', 'KF_VY', 'KF_VZ',
                'KF_Drag', 'Diagnostic_Message'
            ])

        
    def setup_plots(self):
        """Configure all plot widgets with proper settings"""
        color1 = (25,150,207) # Shade of Olin blue for theme
        color2 = (207, 102, 25) # Burnt Orange for contrast
        color3 = (255, 214, 0) # Vibrant Yellow for contrast

        self.plot_config = {
            'Plot1': {
                'title': 'Altitude',
                'vars': ['Baro_Alt', 'KF_Y'],
                'colors': [color1, color2],
                'unit': 'm'
            },
            'Plot2': {
                'title': 'Velocity',
                'vars': ['KF_VY'],
                'colors': [color1],
                'unit': 'm/s'
            },
            'Plot3': {
                'title': 'Orientation',
                'vars': ['Euler_X', 'Euler_Y', 'Euler_Z'],
                'colors': [color1, color2, color3],
                'unit': 'deg'
            },

            'Plot4': {
                'title': 'Linear Acceleration',
                'vars': ['Accel_X', 'Accel_Y', 'Accel_Z'],
                'colors': [color1, color2, color3],
                'unit': 'm/s²'
            },
            'Plot5': {
                'title': 'Angular Velocity',
                'vars': ['Gyro_X', 'Gyro_Y', 'Gyro_Z'],
                'colors': [color1, color2, color3],
                'unit': 'rad/s'
            },
            'Plot6': {
                'title': 'Temperature',
                'vars': ['Temp'],
                'colors': [color1],
                'unit': '°C'
            }
        }

        for plot_name, config in self.plot_config.items():
            plot_widget = getattr(self.ui, plot_name)
            plot_widget.clear()
            plot_widget.setTitle(f"{config['title']} ({config['unit']})", color=(214,230,237), size='12pt')
            plot_widget.addLegend()
            plot_widget.showGrid(x=True, y=True)
            
            config['curves'] = []
            for var, color in zip(config['vars'], config['colors']):
                curve = plot_widget.plot(pen=pg.mkPen(color, width=2), name=var)
                config['curves'].append(curve)

    def initialize_data_structures(self):
        """Initialize data storage structures"""

        self.raw_data = None  # Placeholder for raw data received from the WebSocket

        # Initialize a Pandas DataFrame to store and save data for later use
        # This will be used to save data to a CSV file, *not for plotting*
        self.recorded_data = pd.DataFrame(columns=[
            'time', 'Accel_X', 'Accel_Y', 'Accel_Z', 
            'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Temp',
            'Euler_X', 'Euler_Y', 'Euler_Z', 'Baro_Alt',
            'Longitude', 'Latitude', 'GPS_Alt', 'Phase',
            'Continuity', 'Voltage', 'Link_Strength',
            'KF_X', 'KF_Y', 'KF_Z', 'KF_VX', 'KF_VY', 'KF_VZ',
            'KF_Drag', 'Diagnostic_Message'
        ])

        self.idx = 0 # Index for plot testing
        # example arrays for testing
        self.time = []
        self.Ax = []
        self.Ay = []
        self.Az = []
        self.Gx = []
        self.Gy = []
        self.Gz = []
        self.Vx = []
        self.Vy = []
        self.Vz = []
        self.KFz = []
        self.T = []
        self.Ex = []
        self.Ey = []
        self.Ez = []


        self.max_points = 50 # Max number of data points to display in the plot

        # create empty arrays for each data variable that *will be plotted*
        # stored in a dictionary for easy access
        self.plot_data_dict = {key: [] for key in [
            'time', 'Accel_X', 'Accel_Y', 'Accel_Z', 
            'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Temp',
            'Euler_X', 'Euler_Y', 'Euler_Z', 'Baro_Alt',
            'Longitude', 'Latitude', 'GPS_Alt', 'Phase',
            'Continuity', 'Voltage', 'Link_Strength',
            'KF_X', 'KF_Y', 'KF_Z', 'KF_VX', 'KF_VY', 'KF_VZ',
            'KF_Drag', 'Diagnostic_Message'
        ]}
        
        # Initialize flight phase labels and colors
        self.phase_labels = ["IDLE", "ARMED", "ASCENT", "APOGEE", "DECENT"]
        self.phase_colors = ["77, 86, 88", "0, 148, 255", "0, 103, 192", "173, 216, 230", "0, 168, 150"]

        #  Initialize error statuses in the GUI
        self.errors = [self.ui.IMU_error, self.ui.ALT_error, self.ui.GPS_error]

        # Initialize variables for data rate calculation
        self.last_packet_time = 0  # Total bytes received
        self.data_rate = 0  # Data rate in bytes per second

    def fetch_data(self):
        """Fetch new data and update buffers"""
        self.raw_data = receive.get_data()
        #print(self.raw_data)

        if self.raw_data is not None and self.collect_data:
            self.new_data_signal.emit()  # Emit signal to update the display

            # Store in DataFrame if data is received
            new_row = pd.DataFrame([self.raw_data])
            self.recorded_data = pd.concat([self.recorded_data, new_row], ignore_index=True)

            # Append new data from raw_data to plot_data_dict
            for data in self.raw_data.keys():
                self.plot_data_dict[data].append(self.raw_data[data])
                self.plot_data_dict[data] = self.plot_data_dict[data][-self.max_points:]
            
        # Calculate the time elapsed since the last data rate calculation
        current_time = time.time()
        if self.last_packet_time is not None:
            time_interval = current_time - self.last_packet_time
            if time_interval > 0:
                self.data_rate = 1 / time_interval  # Frequency in Hz
        self.last_packet_time = current_time  # Update the timestamp

    def update_plots(self, plot_name, x, y_dict):
        """
        Update a plot with multiple variables.
        """
        config = self.plot_config[plot_name]
        for i, var in enumerate(config['vars']):
            config['curves'][i].setData(x, y_dict[var])  # Update each curve with new data

    def update_display(self):
        """
        Updates every element of the GUI.
        """

        # Update the plots and display elements with the latest data
        if self.raw_data is None:
            return

        # Update the plots for acceleration (too lazy to do a for loop)
        self.update_plots('Plot1', self.plot_data_dict["time"], {"Baro_Alt": self.plot_data_dict["Baro_Alt"], "KF_Y": self.plot_data_dict["KF_Y"]})
        self.update_plots('Plot2', self.plot_data_dict["time"], {"KF_VY": self.plot_data_dict["KF_VY"]})
        self.update_plots('Plot3', self.plot_data_dict["time"], {"Euler_X": self.plot_data_dict["Euler_X"], "Euler_Y": self.plot_data_dict["Euler_Y"], "Euler_Z": self.plot_data_dict["Euler_Z"]})
        self.update_plots('Plot4', self.plot_data_dict["time"], {"Accel_X": self.plot_data_dict["Accel_X"], "Accel_Y": self.plot_data_dict["Accel_Y"], "Accel_Z": self.plot_data_dict["Accel_Z"]})
        self.update_plots('Plot5', self.plot_data_dict["time"], {"Gyro_X": self.plot_data_dict["Gyro_X"], "Gyro_Y": self.plot_data_dict["Gyro_Y"], "Gyro_Z": self.plot_data_dict["Gyro_Z"]})
        self.update_plots('Plot6', self.plot_data_dict["time"], {"Temp": self.plot_data_dict["Temp"]})

        # Update the display elements with the latest data
        if self.raw_data is not None:
            self.ui.data_rate_val.setText(f"{self.data_rate:.2f} Hz")
            self.ui.lat_val.setText(str(self.raw_data["Latitude"]))
            self.ui.lon_val.setText(str(self.raw_data["Longitude"]))
            #self.ui.alt_val.setText(str(self.raw_data["GPS_Alt"])) # this value can be replaced entirely, probably with drag?
            self.ui.voltage_val.setText(f"{self.raw_data["Voltage"]}V")
            self.ui.RSSI_val.setText(f"{self.raw_data["Link_Strength"]}%")
            #self.ui.diagnostic_message_val.setText(str(self.raw_data["Diagnostic_Message"])) # this needs to be translated into changing an element in the GUI
            #self.ui.continuity_val.setText(str(self.raw_data["Continuity"])) # are these the pyros? need to figure out what data is being sent
            
            # Change the text of the flight phase label to the current phase
            self.ui.flight_phase.setStyleSheet("QLabel {\n"
            "    background-color: rgb(" + self.phase_colors[int(self.raw_data["Phase"])-1]  + ");\n"
            "    border-radius: 5px;\n"
            "    padding: 1px;\n"
            "    color: white;\n"
            "}\n"
            "")
            self.ui.flight_phase.setText(self.phase_labels[int(self.raw_data["Phase"])-1])

            # pyros_val = list(str(self.raw_data["Continuity"]))
            # pyro_display = [int(pyros_val[-2]), int(pyros_val[-3])]
            # if int(pyros_val[-1]) == 1:
            #     pyro_status = "Armed"
            # self.ui.pyros_val.setText(pyro_status + ", " + str(pyro_display))

            # convert Diagnostic_Message to 8 bit binary
            bin_diag = format(int(self.raw_data["Diagnostic_Message"]), '08b')
            # remove the first two characters (0b) and convert to a list of bits
            bin_diag_list = list(bin_diag)
            # loop through the errors and set the color based on current error status
            for i, error in enumerate(self.errors, start=1):
                color = "rgb(25,150,207)" if bin_diag_list[-i]=="0" else "rgb(13,84,142)"
                error.setStyleSheet(f"""
                    QLabel {{
                        background-color: {color};
                        border-radius: 5px;
                        padding: 1px;
                        color: white;
                    }}
                """)

    def closeEvent(self, event):
        '''
        Handle the window close event.
        '''
        # Ask the user for confirmation before closing the application
        reply = QtWidgets.QMessageBox.question(
            self,
            "Exit Application",
            "Are you sure you want to exit?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
        )

        # If the user clicks Yes, close the application
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            event.accept()  # Close the application
            sys.exit(0)
        else:
            event.ignore()  # Ignore the close event

    # button functions
    # connect_toggle handles basic connectivity logic, needs a lot of improvement
    def connect_toggle(self):
        '''
        Toggle the WebSocket connection.
        '''
        if self.connect == 0:  # If not connected, attempt to connect
            self.status = receive.connect_websocket()
            if self.status == "Connected":
                self.connect = 1  # Update the connection state
                self.ui.connect_toggle.setText("Disconnect")
            self.ui.log_entry.appendPlainText(self.status)
        elif self.connect == 1:  # If connected, disconnect
            self.status = receive.disconnect_websocket()
            self.connect = 0  # Update the connection state
            self.ui.connect_toggle.setText("Connect")
            self.ui.log_entry.appendPlainText(self.status)

    def toggle_record_data(self):
        '''
        Toggle the data collection state.
        '''
        if self.collect_data == 0 and self.connect == 1:
            self.log_message = "Data collection started"
            self.collect_data = 1
            self.ui.log_entry.appendPlainText(self.log_message)
            self.ui.mission_start_toggle.setText("Stop Recording")
        elif self.collect_data == 0 and self.connect == 0:
            self.log_message = "No connection established"
            self.ui.log_entry.appendPlainText(self.log_message)
        else:
            self.log_message = "Data collection stopped"
            self.collect_data = 0
            self.ui.log_entry.appendPlainText(self.log_message)
            self.ui.mission_start_toggle.setText("Start Recording")

    def toggle_autosave(self):
        '''
        Toggle the auto save feature for the recorded data.
        '''
        if self.autosave == 0:
            self.autosave = 1
            self.ui.autosave_toggle.setText("Auto Save: On")
            self.ui.log_entry.appendPlainText("Auto save enabled")
        else:
            self.autosave = 0
            self.ui.autosave_toggle.setText("Auto Save: Off")
            self.ui.log_entry.appendPlainText("Auto save disabled")

    def save_recorded_data(self): # saves data to a CSV file
        '''
        Save the collected data to CSV file.
        '''
        # Generate a filename based on the current date and time
        filename = str(datetime.now().strftime("%Y-%m-%d_%H.%M.%S")) + "_flightdata.csv"

        # Check if the recorded data DataFrame is not empty before saving
        if not self.recorded_data.empty:
            self.recorded_data.to_csv(filename, index=False) # Save the DataFrame to a CSV file
            self.ui.log_entry.appendPlainText(f"Data saved to {filename}") # Log the save action
        else:
            self.ui.log_entry.appendPlainText("No data to save.") # Log if no data is available
   
    def clear_recorded_data(self):
        '''
        Clear all recorded data from the plots and the DataFrame.
        '''

        # Clear all recorded data from the plots
        for plot_name, config in self.plot_config.items():
            # Reset the data in the curves
            for curve in config['curves']:
                curve.setData([], [])  # Clear the curve data

        # Clear the data to be plotted
        for key in self.plot_data_dict.keys():
            self.plot_data_dict[key] = []

        # Reset the recorded data DataFrame
        self.recorded_data = pd.DataFrame(columns=[
            'time', 'Accel_X', 'Accel_Y', 'Accel_Z', 
            'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Temp',
            'Euler_X', 'Euler_Y', 'Euler_Z', 'Baro_Alt',
            'Longitude', 'Latitude', 'GPS_Alt', 'Phase',
            'Continuity', 'Voltage', 'Link_Strength',
            'KF_X', 'KF_Y', 'KF_Z', 'KF_VX', 'KF_VY', 'KF_VZ',
            'KF_Drag', 'Diagnostic_Message'
        ])

        self.ui.log_entry.appendPlainText("Data Cleared")
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    #window.showMaximized()
    window.show()
    sys.exit(app.exec())
