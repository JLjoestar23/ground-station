from itertools import islice
import ast

import struct

def deserialize_packet(encoded_data):
    """
    Deserializes a byte stream (encoded_data) into a list of floats.
    
    :param encoded_data: A byte string containing encoded float values.
    :return: A list of floats representing the decoded packet.
    """
    # Make sure the byte data is in the correct format
    # If the length of encoded_data is not a multiple of 4, it's an invalid packet
    if len(encoded_data) % 4 != 0:
        raise ValueError("Encoded data length is not a multiple of 4 (cannot form float values).")
    
    # List to hold the deserialized float values
    decoded_floats = []
    
    # Iterate over the byte stream, 4 bytes at a time (since each float is 4 bytes)
    for i in range(0, len(encoded_data), 4):
        # Extract a 4-byte slice from the data
        byte_slice = encoded_data[i:i+4]
        
        # Use struct to unpack the 4 bytes into a float
        # 'f' format character specifies a single precision float (4 bytes)
        decoded_float = struct.unpack('f', byte_slice)[0]
        
        # Append the decoded float to the list
        decoded_floats.append(decoded_float)
    
    return decoded_floats

# Example usage:
encoded_data = b'\x00\x00\x80\x3F'
  # Example encoded byte stream (representing [3.1415, 2.718])
decoded_floats = deserialize_packet(encoded_data)

print("Decoded floats:", decoded_floats)


