import threading
import customtkinter as tk
import colorsys
import math
from pystray import Icon, MenuItem as item
from PIL import Image, ImageTk, ImageDraw, ImageColor
import serial
import time

arduino = serial.Serial('COM6', 9600)

running_rainbow = False

def create_color_wheel(size=380):
    image = Image.new('RGB', (size, size), color="#252422")
    draw = ImageDraw.Draw(image)

    for angle in range(360):
        color = ImageColor.getrgb(f"hsl({angle}, 100%, 50%)")
        draw.pieslice([0, 0, size, size], start=angle, end=angle + 1, fill=color)
    return image

def get_color_from_position(x, y, size=380):
    center = (size // 2, size // 2)
    dx = x - center[0]
    dy = y - center[1]
    angle = math.degrees(math.atan2(dy, dx)) % 360
    color = ImageColor.getrgb(f"hsl({angle}, 100%, 50%)")
    return color

def send_rgb_to_arduino(rgb):
    """Send RGB values to Arduino via serial."""
    try:
        if arduino.is_open:
            r, g, b = rgb
            arduino.write(bytes([r, g, b])) 
            time.sleep(0.01)  
    except serial.SerialException:
        print("ERROR")
        show_popup

def adjust_brightness(color, brightness):
    r, g, b = color
    brightness_factor = brightness / 100.0  
    r = int(r * brightness_factor)
    g = int(g * brightness_factor)
    b = int(b * brightness_factor)
    return (r, g, b)

def on_motion(event):
    if is_locked or not is_on:  
        return
    x, y = event.x, event.y
    if 0 <= x <= 380 and 0 <= y <= 380:
        color = get_color_from_position(x, y)
        val = brightness_slider.get()
        bricolor = adjust_brightness(color, val)
        send_rgb_to_arduino(bricolor)
        
    color_label.configure( text= color,font=("Arial", 40, "bold"), text_color = "#fffcf2")
    color_label.place(relx=xpos, rely=0.22, anchor="center") 


def on_click(event):
    global is_locked, selected_color
    if is_locked: 
        return
    else:
        x, y = event.x, event.y
        if 0 <= x <= 380 and 0 <= y <= 380:
            is_locked = True  
            selected_color = get_color_from_position(x, y)
            color_label.configure(text=selected_color)
            bright = brightness_slider.get()
            f = adjust_brightness(selected_color, bright)
            send_rgb_to_arduino(f)

def sliderchange(brightness):
    if is_on:
        if selected_color:
            f = adjust_brightness(selected_color, brightness)
            send_rgb_to_arduino(f)

def show_popup():
    popup = tk.CTkToplevel(root)
    popup.geometry("300x150")
    popup.title("Popup Message")

    label = tk.CTkLabel(popup, text="This is a popup!", font=("Arial", 16))
    label.pack(pady=20)

    button = tk.CTkButton(popup, text="OK", command=popup.destroy)
    button.pack(pady=10)


def toggle_button():
    global is_on
    if is_on:
        onoff.configure(text="Off", fg_color="#eb5e28")
        turnoff()
        is_on = False
    else:
        onoff.configure(text="On", fg_color="#5CB85C")
        turnon()
        is_on = True

def changeColor():
    global is_locked
    if  is_on:
        is_locked = False

def hue_to_rgb(hue):
    """Convert a hue value (0-360) to RGB tuple."""
    r, g, b = colorsys.hsv_to_rgb(hue / 360.0, 1.0, 1.0)
    return int(r * 255), int(g * 255), int(b * 255)

def rainbow_effect():
    global running_rainbow
    hue = 0
    while running_rainbow:
        if not is_on:
            return
        if not switchR.get():
            running_rainbow = False
            time.sleep(0.1)
            return 
        
        rgb = hue_to_rgb(hue)
        send_rgb_to_arduino(rgb)
        hue = (hue + 1) % 360 
        time.sleep(0.05)


def rainbowOn():
    global running_rainbow
    if switchR.get():  
        if not running_rainbow: 
            running_rainbow = True
            threading.Thread(target=rainbow_effect, daemon=True).start()
    else:
        if is_on: 
            running_rainbow = False 
            if selected_color:  
                send_rgb_to_arduino(selected_color)
            else:
                send_rgb_to_arduino((0, 0, 0))

def turnoff():
    send_rgb_to_arduino((0,0,0))

def turnon():
    global selected_color
    slider = brightness_slider.get() 
    if selected_color == None:
        selected_color = (0,0,0)  
    newcolor = adjust_brightness(selected_color, slider)
    send_rgb_to_arduino(newcolor)

def restore(icon):
    root.deiconify()
    icon.stop()

def quit():
    root.destroy()

def close():
    root.withdraw()
    tray()

def tray():
    image = Image.open(r"C:\Users\afsal\OneDrive\Desktop\LED\icon.ico")
    icon = Icon("LED Control", image, menu=(item("Quit",quit),item("Restore",action=restore,default=True)))
    threading.Thread(target=icon.run, daemon=True).start()

# Main
root = tk.CTk(fg_color="#252422")
root.title("Color Selector")
root.resizable(False, False)
root.geometry("1129x783")
root.iconbitmap("icon.ico")
root.protocol("WM_DELETE_WINDOW", close)


xpos =0.71
color_wheel = create_color_wheel()
color_wheel_photo = ImageTk.PhotoImage(color_wheel)


color_wheel_label = tk.CTkLabel(root, image=color_wheel_photo, text="")
color_wheel_label.pack(padx=120, pady=10, side="left", anchor="center")
color_label = tk.CTkLabel(root, text="0 0 0",font=("Arial", 40, "bold"),text_color = "#fffcf2" )
color_label.place(relx=xpos, rely=0.22, anchor="center")


selected_label = tk.CTkLabel(
            root,
            text="Selected Color",
            font=("Arial", 12 ), 
            text_color="#fffcf2", 
            anchor="center")
selected_label.place(relx=xpos, rely=0.26, anchor="center")  

brightness_slider = tk.CTkSlider(root, 
                                from_=10,
                                to=100,
                                number_of_steps=101,
                                fg_color="#232529",
                                border_width= 1,
                                border_color="#fffcf2",
                                width=350,
                                height=20,
                                button_color="#eb5e28",
                                hover=True,
                                command = sliderchange)
brightness_slider.set(100)  
brightness_slider.place(relx=xpos, rely=0.39, anchor="center")

selected_label = tk.CTkLabel(
            root,
            text="Brightness",
            font=("Arial", 12 ),  
            text_color="#ffffff", 
            anchor="center")
selected_label.place(relx=xpos, rely=0.43, anchor="center")

switchR = tk.CTkSwitch(root,
                       text="Rainbow Mode",
                       font=("Arial", 20, "bold"),
                       text_color="#fffcf2",
                       button_hover_color="#eb5e28",
                       progress_color="#eb5e28",
                       button_color ="#fffcf2",
                       command=rainbowOn)
switchR.place(relx=xpos, rely=0.57, anchor="center")

is_on = True
onoff = tk.CTkButton(
    root,
    text="Off", 
    command= toggle_button, 
    fg_color="#eb5e28",  
    width=200,
    height=60,
    font=("Arial", 20, "bold"),
    corner_radius = 60)
onoff.place(relx=xpos, rely=0.75, anchor="center")

anothercolor = tk.CTkButton(root,
                            text="Choose Another Color",
                            command=changeColor,
                            text_color="#fffcf2",
                            height=40,
                            font=("Arial", 12),
                            border_color="#fffcf2",
                            hover_color="#eb5e28",
                            border_width=1,
                            corner_radius=60,
                            fg_color="#252422")
anothercolor.place(relx=xpos, rely=0.83, anchor="center")



is_locked =  False
selected_color = None 
color_wheel_label.bind("<Motion>", on_motion)
color_wheel_label.bind("<Button-1>", on_click)


root.mainloop()
