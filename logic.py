from PIL import Image, ImageDraw, ImageColor
import threading
import pyfftw
import time
import numpy as np
from gui import UserInterface


class Logic():

    def __init__(self, root, arduino):
        self.xpos = 0.71
        self.root = root # Create a Tkinter root window
        self.arduino = arduino  # Replace with actual Arduino connection instance
        self.ui = UserInterface(self.root, self.arduino, self) 
        self.running_rainbow = False #flag for rainbow mode
        self.running_ambient = False
        self.is_locked = False #flag for color selection
        self.is_on = True
        self.running_pulse = False
        self.selected_color = (0,0,0)
        self.previous_color = (0, 0, 0)
        self.SAMPLE_RATE =  48000  
        self.CHUNK_SIZE = 1024 
        self.BASS_RANGE = (50, 200)
        self.MIDS_RANGE = (250, 2000)
        self.HIGHS_RANGE = (2000, 20000)
        self.smooth_bass = 0
        self.smooth_mids = 0
        self.smooth_highs = 0
        self.FRAME_RATE = 30

        self.freq = np.fft.fftfreq(self.CHUNK_SIZE, d=1/self.SAMPLE_RATE)[:self.CHUNK_SIZE // 2]
        self.fft_input = pyfftw.empty_aligned(self.CHUNK_SIZE, dtype='float32')
        self.fft_output = pyfftw.empty_aligned(self.CHUNK_SIZE // 2 + 1, dtype='complex64')
        self.fftw_object = pyfftw.FFTW(
            self.fft_input, 
            self.fft_output,
            flags=('FFTW_MEASURE',), 
            threads=2 
        )

        
    def resource_path(self, relative_path):
        import sys
        import os
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
        import math
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
        if self.is_locked or not self.is_on or self.running_rainbow or self.running_pulse or self.running_ambient:  
            return
        x, y = event.x, event.y
        if 0 <= x <= 380 and 0 <= y <= 380:
            color = self.get_color_from_position(x, y)
            val = self.ui.brightness_slider.get()
            bricolor = self.adjust_brightness(color, val)
            self.arduino.send_rgb_to_arduino(bricolor)

        self.ui.color_label.configure(text=color, font=("Arial", 39, "bold"), text_color="#fffcf2")
        self.ui.color_label.place(relx=self.xpos, rely=0.185, anchor="center")
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
                self.ui.color_label.configure(text=self.selected_color)
                bright = self.ui.brightness_slider.get()
                f = self.adjust_brightness(self.selected_color, bright)
                self.arduino.send_rgb_to_arduino(f)
    """Selects the color when left clicks on the color wheel"""

    def sliderchange(self, brightness):
        if self.running_pulse or self.running_ambient or self.running_rainbow:
            return
        if self.is_on:
            if self.selected_color:
                f = self.adjust_brightness(self.selected_color, brightness)
                self.arduino.send_rgb_to_arduino(f)
    """This function adjusts the brightness and send to the Arduino"""

    def toggle_button(self):
        if self.is_on:
            self.ui.onoff.configure(text="Off", fg_color="#eb5e28")
            self.turnoff()
            self.is_on = False
        else:
            self.ui.onoff.configure(text="On", fg_color="#5CB85C")
            self.turnon()
            self.is_on = True
            if self.running_pulse == True:
                self.pulse_on()
        """Toggles on and of Function"""

    def changeColor(self):
        if self.is_on:
            self.is_locked = False

    def hue_to_rgb(self, hue):
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(hue / 360.0, 1.0, 1.0)
        return int(r * 255), int(g * 255), int(b * 255)

    def rainbow_effect(self):
        hue = 0

        while self.running_rainbow:
            if not self.is_on:
                return

            if not self.ui.switchR.get():
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
        if self.ui.switchR.get() and not self.running_pulse and not self.running_ambient:  
            if not self.running_rainbow: 
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
            if self.running_rainbow or self.running_ambient:
                return
            self.running_pulse = True
            self.stream = self.start_stream()
            self.stream.start()
            
    def pulse_off(self):
        self.running_pulse = False
        if hasattr(self, 'stream') and self.stream is not None:
            self.stream.stop()  
            self.stream.close()
        if self.selected_color is None:
            self.arduino.send_rgb_to_arduino((0, 0, 0))
        else:
            self.arduino.send_rgb_to_arduino(self.selected_color)

    def toggle_pulsating_mode(self):
        if self.ui.switchP.get():
            if self.is_on:
                self.pulse_on()
        else:
            self.pulse_off()

    def start_stream(self):
        import sounddevice as sd
        return sd.Stream(
            device=(None, None),  
            samplerate=self.SAMPLE_RATE,
            blocksize=self.CHUNK_SIZE,
            channels=2,
            callback=self.audio_callback,
            latency="low")


    def audio_callback(self, input, output, frames, time, status):
        if status:
            print(status)

        output[:] = input
        audio_data = np.mean(input, axis=1).astype(np.float32) 

        self.fft_input[:] = audio_data
        self.fftw_object() 
        freq_magnitude = np.abs(self.fft_output[:self.CHUNK_SIZE // 2])
        
        self.bass_level = np.sum(freq_magnitude[(self.freq >= self.BASS_RANGE[0]) & (self.freq < self.BASS_RANGE[1])])
        self.mids_level = np.sum(freq_magnitude[(self.freq >= self.MIDS_RANGE[0]) & (self.freq < self.MIDS_RANGE[1])])
        self.highs_level = np.sum(freq_magnitude[(self.freq >= self.HIGHS_RANGE[0]) & (self.freq < self.HIGHS_RANGE[1])])

        self.smooth_bass = max(self.smooth_bass*0.85, self.bass_level)
        self.smooth_mids = max(self.smooth_mids*0.85, self.mids_level)
        self.smooth_highs = max(self.smooth_highs*0.85, self.highs_level)

        bass_scaled = int(np.clip((self.smooth_bass / 90) * 255, 0, 255))
        mids_scaled = int(np.clip((self.smooth_mids / 800) * 255, 0, 255))
        highs_scaled = int(np.clip((self.smooth_highs /1600)* 255, 0, 255))

        rgb = (bass_scaled, mids_scaled,highs_scaled)
        self.arduino.send_rgb_to_arduino(rgb)


    def toggle_ambient(self):
            if self.ui.switchA.get() and self.is_on:
                if self.is_on:
                    self.running_ambient = True
                    self.AmbientMode()
            else:
                self.ambientOff()

    def ambientOff(self):
            self.running_ambient = False
            self.arduino.send_rgb_to_arduino(self.selected_color)
    
    def AmbientMode(self):
        if not self.running_ambient or self.running_pulse or self.running_rainbow:
            return

        thread = threading.Thread(target=self.ambient_loop, daemon=True)
        thread.start()

    def ambient_loop(self):
        
        import mss
        while self.running_ambient:
            with mss.mss() as screenCapture:
                DIMENSIONS = {'left':0, 'top':0, 'width': 640, 'height':480}
                ss = screenCapture.grab(DIMENSIONS)
                img = Image.frombytes("RGB", ss.size, ss.rgb)
                colors = img.quantize(colors=1, method=0, dither=0)
                palette = colors.getpalette()
                r,g,b = (palette[:3])
                new_color = self.exp_smooth(self.previous_color, (r,g,b), 0.75) 
                self.arduino.send_rgb_to_arduino(new_color)
                self.previous_color = (new_color)
            time.sleep(1/self.FRAME_RATE)

    def exp_smooth(self, prev_color, new_color, alpha):
        return tuple(int(prev * (1 - alpha) + curr * alpha) for prev, curr in zip(prev_color, new_color))

    def averageColor(self, image):
        average_colors = np.mean(image, axis=(0,1))
        in_rgb = average_colors[::-1]
        return tuple(map(int, in_rgb))    


    
    def turnoff(self):
        self.running_pulse = False
        self.running_rainbow = False
        if self.running_pulse:
            self.pulse_off()
        self.arduino.send_rgb_to_arduino((0, 0, 0))

    def turnon(self):
        slider = self.ui.brightness_slider.get() 
        newcolor = self.adjust_brightness(self.selected_color, slider)
        self.arduino.send_rgb_to_arduino(newcolor)

    def restore(self, icon):
        self.ui.root.deiconify()
        icon.stop()

    def quit(self):
        self.arduino.send_rgb_to_arduino((0, 0, 0))
        self.arduino.arduino.close()
        self.ui.root.destroy()

    def close(self):
        self.ui.root.withdraw()
        self.tray()

    def tray(self):
        from pystray import Icon, MenuItem as item
        image = Image.open(self.resource_path("icon.ico"))
        icon = Icon("LED Control", image, menu=(item("Restore", action=self.restore, default=True), item("Quit", self.quit)))