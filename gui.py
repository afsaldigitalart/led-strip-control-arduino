import customtkinter as ctk
from PIL import ImageTk



class UserInterface():
    def __init__(self, root, arduino_connection, logic):
        self.root = root
        self.logic = logic
        self.xpos = 0.71 #allingment of Labels, Slider and Buttons in X Axis
        # self.output_device = self.get_audio_output_device()

        self.arduino = arduino_connection 
        self.root.title("Color Selector")
        self.root.resizable(False, False)
        self.root.geometry("1129x783")
        self.root.iconbitmap(self.logic.resource_path("icon.ico"))
        self.root.protocol("WM_DELETE_WINDOW", self.logic.close)
        self.UIwidgets()

    def UIwidgets(self):
            color_wheel = self.logic.create_color_wheel()
            self.color_wheel_photo = ImageTk.PhotoImage(color_wheel)

            self.color_wheel_label = ctk.CTkLabel(self.root, image=self.color_wheel_photo, text="") 
            self.color_wheel_label.pack(padx=120, pady=10, side="left", anchor="center")

            self.color_label = ctk.CTkLabel(self.root, text="0 0 0",font=("Arial", 40, "bold"),text_color = "#fffcf2" )
            self.color_label.place(relx=self.xpos, rely=0.22, anchor="center")
            #The above code displays the color wheel

            self.selected_text = ctk.CTkLabel(
                self.root,
                text="Selected Color",
                font=("Arial", 12),
                text_color="#fffcf2",
                anchor="center")
            self.selected_text.place(relx=self.xpos, rely=0.26, anchor="center")
            #For the "Selected Color Text"
            
            self.brightness_slider = ctk.CTkSlider(self.root, 
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
                command=self.logic.sliderchange)
            self.brightness_slider.set(100)
            self.brightness_slider.place(relx=self.xpos, rely=0.39, anchor="center")
            self.selected_label = ctk.CTkLabel(
                self.root,
                text="Brightness",
                font=("Arial", 12),
                text_color="#ffffff",
                anchor="center")
            self.selected_label.place(relx=self.xpos, rely=0.43, anchor="center")
            #Brightness Slider and Text

            self.switchR = ctk.CTkSwitch(self.root,
                text="Rainbow Mode",
                font=("Arial", 20, "bold"),
                text_color="#fffcf2",
                button_hover_color="#eb5e28",
                progress_color="#eb5e28",
                button_color="#fffcf2",
                command= self.logic.rainbowOn
                )
            self.switchR.place(relx=self.xpos, rely=0.54, anchor="center")
            #Toggle Button for Rainbow Mode

            self.switchP = ctk.CTkSwitch(self.root,
                text="Pulsating Mode",
                font=("Arial", 20, "bold"),
                text_color="#fffcf2",
                button_hover_color="#eb5e28",
                progress_color="#eb5e28",
                button_color="#fffcf2",
                command=self.logic.toggle_pulsating_mode
                )
            self.switchP.place(relx=self.xpos, rely=0.62, anchor="center")
            #Toggle Button for Rainbow Mode


            self.switchA = ctk.CTkSwitch(self.root,
                text="Ambient Mode",
                font=("Arial", 20, "bold"),
                text_color="#fffcf2",
                button_hover_color="#eb5e28",
                progress_color="#eb5e28",
                button_color="#fffcf2",
                command=self.logic.toggle_ambient
                )
            self.switchA.place(relx=self.xpos, rely=0.67, anchor="center")

            self.onoff = ctk.CTkButton(
                self.root,
                text="Off", 
                 
                fg_color="#eb5e28",
                width=200,
                height=60,
                font=("Arial", 20, "bold"),
                corner_radius=60,
                command=self.logic.toggle_button)
            self.onoff.place(relx=self.xpos, rely=0.75, anchor="center")
            #ON/OFF Button

            anothercolor = ctk.CTkButton(self.root,
                text="Choose Another Color",
                
                text_color="#fffcf2",
                height=40,
                font=("Arial", 12),
                border_color="#fffcf2",
                hover_color="#eb5e28",
                border_width=1,
                corner_radius=60,
                fg_color="#252422",
                command=self.logic.changeColor)
            anothercolor.place(relx=self.xpos, rely=0.83, anchor="center")
            #Button to enable user to select another color once a color is selected already

            self.color_wheel_label.bind("<Motion>", self.logic.on_motion)
            self.color_wheel_label.bind("<Button-1>", self.logic.on_click)
            #For tracking mouse movements and show the color in real time
