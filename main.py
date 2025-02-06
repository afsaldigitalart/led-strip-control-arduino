import threading
import customtkinter as tk
import colorsys
import math
import sys
import os
from pystray import Icon, MenuItem as item
from PIL import Image, ImageTk, ImageDraw, ImageColor
import serial.tools.list_ports 
import serial
import time
import sounddevice as sd
import numpy as np

"""The Sotware is a personal project I did to learn more about Arduino. But eventually I learnt
the CTKinter module also. It was a great learning experience and I will be adding more features
as time goes by"""


class LEDstrip():

    def __init__(self, root):
        self.root = root
        self.xpos = 0.71 #allingment of Labels, Slider and Buttons in X Axis
        self.running_rainbow = False #flag for rainbow mode
        self.is_locked = False #flag for color selection
        self.is_on = True
        self.running_pulse = False
        self.SAMPLE_RATE = 44100  
        self.CHUNK_SIZE = 1024 
        self.BASS_RANGE = (50, 200)
        self.MIDS_RANGE = (250, 2000)
        self.HIGHS_RANGE = (2000, 20000)
        self.smooth_bass = 0
        self.smooth_mids = 0
        self.smooth_highs = 0
        # self.output_device = self.get_audio_output_device()

        self.arduino = Arduino() 
        self.root.title("Color Selector")
        self.root.resizable(False, False)
        self.root.geometry("1129x783")
        self.root.iconbitmap(self.resource_path("icon.ico"))
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.UIwidgets()

    def UIwidgets(self):
        color_wheel = self.create_color_wheel()
        self.color_wheel_photo = ImageTk.PhotoImage(color_wheel)

        self.color_wheel_label = tk.CTkLabel(self.root, image=self.color_wheel_photo, text="") 
        self.color_wheel_label.pack(padx=120, pady=10, side="left", anchor="center")

        self.color_label = tk.CTkLabel(root, text="0 0 0",font=("Arial", 40, "bold"),text_color = "#fffcf2" )
        self.color_label.place(relx=self.xpos, rely=0.22, anchor="center")
        #The above code displays the color wheel

        self.selected_text = tk.CTkLabel(
            self.root,
            text="Selected Color",
            font=("Arial", 12),
            text_color="#fffcf2",
            anchor="center")
        self.selected_text.place(relx=self.xpos, rely=0.26, anchor="center")
        #For the "Selected Color Text"
        
        self.brightness_slider = tk.CTkSlider(self.root, 
            from_=10,
            to=100,
            number_of_steps=101,
            fg_color="#232529",
            border_width=1,
            border_color="#fffcf2",
            width=350,
            height=20,
            button_color="#eb5e28",
            hover=True,
            command=self.sliderchange)
        self.brightness_slider.set(100)
        self.brightness_slider.place(relx=self.xpos, rely=0.39, anchor="center")
        self.selected_label = tk.CTkLabel(
            self.root,
            text="Brightness",
            font=("Arial", 12),
            text_color="#ffffff",
            anchor="center")
        self.selected_label.place(relx=self.xpos, rely=0.43, anchor="center")
        #Brightness Slider and Text

        self.switchR = tk.CTkSwitch(self.root,
            text="Rainbow Mode",
            font=("Arial", 20, "bold"),
            text_color="#fffcf2",
            button_hover_color="#eb5e28",
            progress_color="#eb5e28",
            button_color="#fffcf2",
            command=self.rainbowOn)
        self.switchR.place(relx=self.xpos, rely=0.54, anchor="center")
        #Toggle Button for Rainbow Mode

        self.switchP = tk.CTkSwitch(self.root,
            text="Pulsating Mode",
            font=("Arial", 20, "bold"),
            text_color="#fffcf2",
            button_hover_color="#eb5e28",
            progress_color="#eb5e28",
            button_color="#fffcf2",
            command=self.toggle_pulsating_mode)
        self.switchP.place(relx=self.xpos, rely=0.62, anchor="center")
        #Toggle Button for Rainbow Mode

        self.onoff = tk.CTkButton(
            self.root,
            text="Off", 
            command=self.toggle_button, 
            fg_color="#eb5e28",
            width=200,
            height=60,
            font=("Arial", 20, "bold"),
            corner_radius=60)
        self.onoff.place(relx=self.xpos, rely=0.75, anchor="center")
        #ON/OFF Button

        anothercolor = tk.CTkButton(self.root,
            text="Choose Another Color",
            command=self.changeColor,
            text_color="#fffcf2",
            height=40,
            font=("Arial", 12),
            border_color="#fffcf2",
            hover_color="#eb5e28",
            border_width=1,
            corner_radius=60,
            fg_color="#252422")
        anothercolor.place(relx=self.xpos, rely=0.83, anchor="center")
        #Button to enable user to select another color once a color is selected already

        self.color_wheel_label.bind("<Motion>", self.on_motion)
        self.color_wheel_label.bind("<Button-1>", self.on_click)
        #For tracking mouse movements and show the color in real time

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    #To get absolute path. Using this to avoid error while using PyInstaller

    def create_color_wheel(self, size=380):
        image = Image.new('RGB', (size, size), color="#252422")
        draw = ImageDraw.Draw(image)

        for angle in range(360):
            color = ImageColor.getrgb(f"hsl({angle}, 100%, 50%)")
            draw.pieslice([0, 0, size, size], start=angle, end=angle + 1, fill=color)
        return image
    """This function creates a color wheel using Pillow module. Each angle is taken as hue and a pie
    slice is created. This pie slice is filled with cooresponding hue""" 

    def get_color_from_position(self, x, y, size=380):
        center = (size // 2, size // 2)
        dx = x - center[0]
        dy = y - center[1]
        angle = math.degrees(math.atan2(dy, dx)) % 360
        color = ImageColor.getrgb(f"hsl({angle}, 100%, 50%)")
        return color
    """This function fetches mouses position and calculates the distance from the centre. Using that 
    data, the angle is calculated, hence hue. It returns the color color data"""

    def adjust_brightness(self, color, brightness):
        r, g, b = color
        brightness_factor = brightness / 100.0  
        r = int(r * brightness_factor)
        g = int(g * brightness_factor)
        b = int(b * brightness_factor)
        return (r, g, b)
    """Control the brighness of the light by returning the the selected colors 1/(10 to 100) th 
    value. Returns a tuple"""

    def on_motion(self, event):
        if self.is_locked or not self.is_on or self.running_rainbow or self.running_pulse:  
            return
        x, y = event.x, event.y
        if 0 <= x <= 380 and 0 <= y <= 380:
            color = self.get_color_from_position(x, y)
            val = self.brightness_slider.get()
            bricolor = self.adjust_brightness(color, val)
            self.arduino.send_rgb_to_arduino(bricolor)

        self.color_label.configure(text=color, font=("Arial", 40, "bold"), text_color="#fffcf2")
        self.color_label.place(relx=self.xpos, rely=0.22, anchor="center")
    """Checks the mouse data and if the mouse is hovering above the color wheel, it returns the
    corresponding colors"""

    def on_click(self, event): 
        if self.is_locked or self.running_rainbow or self.running_pulse: 
            return

        else:
            x, y = event.x, event.y
            if 0 <= x <= 380 and 0 <= y <= 380:
                self.is_locked = True  
                self.selected_color = self.get_color_from_position(x, y)
                self.color_label.configure(text=self.selected_color)
                bright = self.brightness_slider.get()
                f = self.adjust_brightness(self.selected_color, bright)
                self.arduino.send_rgb_to_arduino(f)
    """Selects the color when left clicks on the color wheel"""

    def sliderchange(self, brightness):
        if self.is_on:
            if self.selected_color:
                f = self.adjust_brightness(self.selected_color, brightness)
                self.arduino.send_rgb_to_arduino(f)
    """This function adjusts the brightness and send to the Arduino"""

    def toggle_button(self):
        if self.is_on:
            self.onoff.configure(text="Off", fg_color="#eb5e28")
            self.turnoff()
            self.is_on = False
        else:
            self.onoff.configure(text="On", fg_color="#5CB85C")
            self.turnon()
            self.is_on = True
            if self.running_pulse == True:
                self.pulse_on()
        """Toggles on and of Function"""

    def changeColor(self):
        if self.is_on:
            self.is_locked = False

    def hue_to_rgb(self, hue):
        r, g, b = colorsys.hsv_to_rgb(hue / 360.0, 1.0, 1.0)
        return int(r * 255), int(g * 255), int(b * 255)

    def rainbow_effect(self):
        hue = 0

        while self.running_rainbow:
            if not self.is_on:
                return

            if not self.switchR.get():
                self.running_rainbow = False
                time.sleep(0.1)
                return 

            rgb = self.hue_to_rgb(hue)
            self.arduino.send_rgb_to_arduino(rgb)
            hue = (hue + 1) % 360 
            time.sleep(0.05)
        """This works by constalntly looping the hue from o-360 until the running_rainbow
        yeilds Flase"""

    def rainbowOn(self):
        if self.switchR.get():  
            if not self.running_rainbow and not self.running_pulse: 
                self.running_rainbow = True
                threading.Thread(target=self.rainbow_effect, daemon=True).start()
        else:
            if self.is_on: 
                self.running_rainbow = False 
                if self.selected_color:  
                    self.arduino.send_rgb_to_arduino(self.selected_color)
                else:
                    self.turnoff()

    def pulse_on(self):
            self.running_pulse = True
            self.stream = self.start_stream()
            self.stream.start()
            
    def pulse_off(self):
            self.running_pulse = False
            self.stream.stop()  
            self.stream.close()
            if self.selected_color:
                self.arduino.send_rgb_to_arduino(self.selected_color)

    def toggle_pulsating_mode(self):
        if self.switchP.get():
            if self.is_on:
                self.pulse_on()
        else:
            self.pulse_off()

    def start_stream(self):
        return sd.Stream(
            device=(None, None),  
            samplerate=self.SAMPLE_RATE,
            blocksize=self.CHUNK_SIZE,
            channels=2,
            callback=self.audio_callback)


    def audio_callback(self, input, output, frames, time, status):
        if status:
            print(status)

        output[:] = input
        audio_data = np.mean(input, axis=1) 

        fft_result = np.fft.fft(audio_data)
        freq_magnitude = np.abs(fft_result[:len(fft_result) // 2])  
        freqs = np.fft.fftfreq(len(fft_result), d=1/self.SAMPLE_RATE)[:len(fft_result) // 2]  

        self.bass_level = np.sum(freq_magnitude[(freqs >= self.BASS_RANGE[0]) & (freqs < self.BASS_RANGE[1])])
        self.mids_level = np.sum(freq_magnitude[(freqs >= self.MIDS_RANGE[0]) & (freqs < self.MIDS_RANGE[1])])
        self.highs_level = np.sum(freq_magnitude[(freqs >= self.HIGHS_RANGE[0]) & (freqs < self.HIGHS_RANGE[1])])

        self.smooth_bass = max(self.smooth_bass*0.85, self.bass_level)
        self.smooth_mids = max(self.smooth_mids*0.85, self.mids_level)
        self.smooth_highs = max(self.smooth_highs*0.85, self.highs_level)

        bass_scaled = int(np.clip((self.smooth_bass / 90) * 255, 0, 255))
        mids_scaled = int(np.clip((self.smooth_mids / 800) * 255, 0, 255))
        highs_scaled = int(np.clip((self.smooth_highs /1600)* 255, 0, 255))

        rgb = (bass_scaled, mids_scaled,highs_scaled)
        self.arduino.send_rgb_to_arduino(rgb)
    
    def turnoff(self):
        self.running_pulse = False
        self.running_rainbow = False
        self.pulse_off()
        
        self.arduino.send_rgb_to_arduino((0, 0, 0))

    def turnon(self):
        slider = self.brightness_slider.get() 
        newcolor = self.adjust_brightness(self.selected_color, slider)
        self.arduino.send_rgb_to_arduino(newcolor)

    def restore(self, icon):
        self.root.deiconify()
        icon.stop()

    def quit(self):
        self.arduino.send_rgb_to_arduino((0, 0, 0))
        self.arduino.arduino.close()
        self.root.destroy()

    def close(self):
        self.root.withdraw()
        self.tray()

    def tray(self):
        image = Image.open(r"C:\Users\afsal\OneDrive\Desktop\LED\icon.ico")
        icon = Icon("LED Control", image, menu=(item("Restore", action=self.restore, default=True), item("Quit", self.quit)))
        threading.Thread(target=icon.run, daemon=True).start()




class Arduino():
    def __init__(self):
        #Connects to the Arduino
        Port = self.checkPort()
        self.arduino = serial.Serial(self.checkPort(), 9600)

    def send_rgb_to_arduino(self, rgb):
        """This Function send the collected RGB values to arduino in 
        Binary Format"""
        try:
            if self.arduino.is_open:
                r, g, b = rgb
                self.arduino.write(bytes([r, g, b])) 
                time. sleep(0.01)  

        except serial.SerialException:
            print("ERROR")

    def checkPort(self):
        """Automatically checks in which port the Arduino is connected
        Error handling to be added"""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "Arduino" in port.description:
                return port.device
        return False
    
#Main Function
if __name__ == "__main__":
    root = tk.CTk(fg_color="#252422")
    main = LEDstrip(root)
    root.mainloop()