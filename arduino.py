import serial.tools.list_ports 
import serial
import time


class Arduino():
    def __init__(self):
        #Connects to the Arduino
        self.port = self.checkPort()
        self.arduino = serial.Serial(self.port, 9600)

    def send_rgb_to_arduino(self, rgb):
        """This Function send the collected RGB values to arduino in 
        Binary Format"""
        try:
            if self.arduino.is_open:
                r, g, b = rgb
                self.arduino.write(bytes([r, g, b])) 
                time. sleep(0.01)  

        except serial.SerialException:
            pass

    def checkPort(self):
        """Automatically checks in which port the Arduino is connected
        Error handling to be added"""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "Arduino" in port.description:
                return port.device 
        return None