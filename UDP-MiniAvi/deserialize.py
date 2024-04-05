import socket
from itertools import islice
import ast

class DataHandler:
    def __init__(self):
        self.data = None
        self.buffer = [] # Initialize a buffer so that self.data doesn't get overwritten when updating. This accumulates data packets
    
    def socket_to_receive_data(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            HOST = '0.0.0.0'
            PORT = 4210
            s.bind((HOST, PORT))
            while True: # while the connection is ongoing
                self.data, _ = s.recvfrom(1024) # _ = addr which we don't care about
                if not self.data: break ### THIS IS A SCAFFHOLD - WHAT IS PROPER EXIT CONDITION?
                self.buffer.append(self.data)
    
    def process_data(self):
        with open('logfile.txt', 'ab') as file:
            for data_packet in self.buffer: # Need to ensure that we're
                file.write(data_packet + b'\n')
            self.buffer.clear()
    
    def split_data_list(self):
        output = []
        # self.buffer is a list so we need to loop through it to get individual strings
        for data_packet in self.buffer:
            decoded_string = data_packet.decode('utf-8') # because we're receiving a byte string we need to decode with a format
            actual_list = ast.literal_eval(decoded_string) # evaluate the string so it becomes a list of this decoded string
            length_to_split = [1] * len(actual_list) # split the input array at each data point
            iter_input = iter(actual_list) 
            # Takes an iterator and number (elem) and returns an iterator (list) that has elem # of elements in it
            sublist = [list(islice(iter_input, 1)) for _ in length_to_split]
            output.extend(sublist)
        return output
    
    # We pass the output from split_data_list and convert these values to a float
    def convert_to_float(self, output):
        # When we pass output to this function it's a 2D list
        flatten_list = [flat for item in output for flat in item] # return only the string in the flattened list
        converted_values = list()
        # the equivalent would be taking in data
        for item in flatten_list: 
            converted_values.append(float(item))
        return converted_values

### CODE THAT WOULD INSTANTIATE CLASS SO WE CAN PASS LIST OF VALUES TO THE float_to_dict() function
    
# creating a separate function for dictionary because it's dependent on the class being called
def float_to_dict(float_list):
    # This function contains the dictionary of array values from the ESP32 which will get passed into visualuzation
    # In order to access the values use syntax dictviz['Key']. Use these to plot
    dictviz = {
        'Current Time' : float_list[0],
        'Accelerometer X Direction' : float_list[1],
        'Accelerometer Y Direction' : float_list[2],
        'Accelerometer Z Direction' : float_list[3],
        'Gyroscope X Direction' : float_list[4],
        'Gyroscope Y Direction' : float_list[5],
        'Gyroscope Z Direction' : float_list[6],
        'Temperature' : float_list[7],
        'Euler X' : float_list[8],
        'Euler Y' : float_list[9],
        'Euler Z' : float_list[10],
        'Barometric Altitude' : float_list[11], # confirm correct key
        'Longitude' : float_list[12],
        'Latitude' : float_list[13],
        'GPS Altitude' : float_list[14],
        '' : float_list[15], # confirm phs
        '' : float_list[16],
        'Voltage' : float_list[17],
        'Link' : float_list[18],
        'Kalman Filter X' : float_list[19],
        'Kalman Filter Y' : float_list[20],
        'Kalman Filter Z' : float_list[21],
        'Kalman Filter Vx' : float_list[22], # confirm
        'Kalman Filter Vy' : float_list[23], # confirm
        'Kalman Filter Vz' : float_list[24], # confirm
        'Kalman Filter Draf' : float_list[25],
        '' : float_list[26], # confirm
        'Diag Msg' : float_list[27], # confirm
    }

    return dictviz