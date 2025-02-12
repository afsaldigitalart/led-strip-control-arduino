import customtkinter as tk
import arduino
from logic import Logic


arduino_connection = arduino.Arduino()
root = tk.CTk(fg_color="#252422")
logic = Logic(root, arduino_connection)


def main(root):
    # UserInterface(root, arduino_connection, logic)
    root.mainloop()


if __name__ == "__main__":
    main(root)

