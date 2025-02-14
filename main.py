import customtkinter as tk
import arduino
from logic import Logic


arduino_connection = arduino.Arduino()
root = tk.CTk()
logic = Logic(root, arduino_connection)


if __name__ == "__main__":
    root.mainloop()

