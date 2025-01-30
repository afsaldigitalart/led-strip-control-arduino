import threading
import customtkinter as tk
import colorsys
import math
import tkinter as tkk
from customtkinter import CTkImage
from pystray import Icon, MenuItem as item
from PIL import Image, ImageTk, ImageDraw, ImageColor
import serial
import time


class LEDstrip():

    def __init__(self, root):
        self.root = root
        self.xpos = 0.71
        self.running_rainbow = False
        self.is_locked = False
        self.selected_color = None
        self.is_on = True

        self.arduino = Arduino() 
        self.root.title("Color Selector")
        self.root.resizable(False, False)
        self.root.geometry("1129x783")
        self.root.iconbitmap("icon.ico")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.UIwidgets()

    def UIwidgets(self):
        color_wheel = self.create_color_wheel()
        self.color_wheel_photo = ImageTk.PhotoImage(color_wheel)

        self.color_wheel_label = tk.CTkLabel(self.root, image=self.color_wheel_photo, text="") 
        self.color_wheel_label.pack(padx=120, pady=10, side="left", anchor="center")

        color_label = tk.CTkLabel(root, text="0 0 0",font=("Arial", 40, "bold"),text_color = "#fffcf2" )
        color_label.place(relx=self.xpos, rely=0.22, anchor="center")
        
        self.selected_label = tk.CTkLabel(
            self.root,
            text="Selected Color",
            font=("Arial", 12),
            text_color="#fffcf2",
            anchor="center")
        self.selected_label.place(relx=self.xpos, rely=0.26, anchor="center")

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

        self.switchR = tk.CTkSwitch(self.root,
            text="Rainbow Mode",
            font=("Arial", 20, "bold"),
            text_color="#fffcf2",
            button_hover_color="#eb5e28",
            progress_color="#eb5e28",
            button_color="#fffcf2",
            command=self.rainbowOn)
        self.switchR.place(relx=self.xpos, rely=0.57, anchor="center")

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

        self.color_wheel_label.bind("<Motion>", self.on_motion)
        self.color_wheel_label.bind("<Button-1>", self.on_click)

    def create_color_wheel(self, size=380):
        image = Image.new('RGB', (size, size), color="#252422")
        draw = ImageDraw.Draw(image)

        for angle in range(360):
            color = ImageColor.getrgb(f"hsl({angle}, 100%, 50%)")
            draw.pieslice([0, 0, size, size], start=angle, end=angle + 1, fill=color)
        return image

    def get_color_from_position(self, x, y, size=380):
        center = (size // 2, size // 2)
        dx = x - center[0]
        dy = y - center[1]
        angle = math.degrees(math.atan2(dy, dx)) % 360
        color = ImageColor.getrgb(f"hsl({angle}, 100%, 50%)")
        return color

    def adjust_brightness(self, color, brightness):
        r, g, b = color
        brightness_factor = brightness / 100.0  
        r = int(r * brightness_factor)
        g = int(g * brightness_factor)
        b = int(b * brightness_factor)
        return (r, g, b)

    def on_motion(self, event):
        if self.is_locked or not self.is_on or self.running_rainbow:  
            return
        x, y = event.x, event.y
        if 0 <= x <= 380 and 0 <= y <= 380:
            color = self.get_color_from_position(x, y)
            val = self.brightness_slider.get()
            bricolor = self.adjust_brightness(color, val)
            self.arduino.send_rgb_to_arduino(bricolor)

        self.color_label.configure(text=color, font=("Arial", 40, "bold"), text_color="#fffcf2")
        self.color_label.place(relx=self.xpos, rely=0.22, anchor="center")

    def on_click(self, event): 
        if self.is_locked: 
            return

        else:
            x, y = event.x, event.y
            if 0 <= x <= 380 and 0 <= y <= 380:
                self.is_locked = True  
                self.selected_color = self.get_color_from_position(x, y)
                self.color_label.configure(text=str(self.selected_color))
                bright = self.brightness_slider.get()
                f = self.adjust_brightness(self.selected_color, bright)
                self.arduino.send_rgb_to_arduino(f)

    def sliderchange(self, brightness):
        if self.is_on:
            if self.selected_color:
                f = self.adjust_brightness(self.selected_color, brightness)
                self.arduino.send_rgb_to_arduino(f)

    def toggle_button(self):
        if self.is_on:
            self.onoff.configure(text="Off", fg_color="#eb5e28")
            self.turnoff()
            self.is_on = False
        else:
            self.onoff.configure(text="On", fg_color="#5CB85C")
            self.turnon()
            self.is_on = True

    def changeColor(self):
        global is_locked
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

    def rainbowOn(self):
        if self.switchR.get():  
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

    def turnoff(self):
        self.arduino.send_rgb_to_arduino((0, 0, 0))

    def turnon(self):
        slider = self.brightness_slider.get()
        if self.selected_color is None:
            self.selected_color = (0, 0, 0)  
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
        self.arduino = serial.Serial('COM6', 9600)

    def send_rgb_to_arduino(self, rgb):
        try:
            if self.arduino.is_open:
                r, g, b = rgb
                self.arduino.write(bytes([r, g, b])) 
                time.sleep(0.01)  

        except serial.SerialException:
            print("ERROR")


if __name__ == "__main__":
    root = tk.CTk(fg_color="#252422")
    main = LEDstrip(root)
    root.mainloop()