
# ![App Icon](icon.ico) Arduino  Led Strip Controller

This project is a Python-based application that allows users to control an LED strip connected to an Arduino. The application provides a graphical user interface (GUI) for selecting colors, adjusting brightness, and enabling various lighting modes such as Rainbow, Pulsating, and Ambient. The application communicates with the Arduino via a serial connection to send RGB values.

__Strictly personal program. For personal learning purpose only__

## Requirements
To run this application, you need the following Python packages:

- customtkinter
- Pillow
- pystray
- numpy
- sounddevice
- mss
- opencv-python
- pyserial

You can install these packages using pip:
```
pip install requirements.txt
```
## Features

- **Color Selection**: Users can select colors from a color wheel.

- **Brightness Control**: Adjust the brightness of the selected color using a slider.

- **Lighting Modes**:

    **Rainbow Mode**: Cycles through a spectrum of colors.

    **Pulsating Mode**: Changes the LED color based on audio input (bass, mids, highs).

    **Ambient Mode**: Matches the LED color to the average color of the screen.

- **On/Off Control**: Turn the LED strip on or off.

- **System Tray Integration**: Minimize the application to the system tray.

![User Interface](https://github.com/user-attachments/assets/cec79ba7-ed32-4761-b74e-42cd38c7daeb)
                  User Interface of the Software

![Screenshot 2025-02-16 222726](https://github.com/user-attachments/assets/aa1cb870-ccca-4f28-b0b6-dff7b82f9a7d)
                  Tray Functionality
         
## File Overview

### main.py
- **Purpose**: Entry point of the application.

- **Key Functions**:

    - Initializes the Arduino connection.

    - Creates the main application window.

    - Starts the main event loop.



### arduino.py
- **Purpose**: Intializes and connect to the Arduino.

- **Key Functions**:

    ____init__ __: Initializes the connection to the Arduino.

    __send_rgb_to_arduino__: Sends RGB values to the Arduino.

    __checkPort__: Automatically detects the port where the Arduino is connected.

### gui.py
- **Purpose**: Manages the graphical user interface.

- **Key Functions**:
    - __Color Wheel__: Displays a color wheel for color selection.

    - __Brightness Slider__: Allows users to adjust the brightness.

    - __Mode Switches__: Toggles for Rainbow, Pulsating, and Ambient modes.

    - __On/Off Button__: Controls the power state of the LED strip.

    - __Quit Button__: Exits the application.

### logic.py
- **Purpose**:  Implements the core logic of the application.

- **Key Functions**:
    - __create_color_wheel__: Generates a color wheel image.

    - __get_color_from_position__: Determines the color based on mouse position.

    - __adjust_brightness__: Adjusts the brightness of the selected color.

    - __rainbow_effect__: Implements the Rainbow mode.

    - __pulse_on/pulse_off__: Implements the Pulsating mode based on audio input.

    - __AmbientMode__: Implements the Ambient mode by matching the screen's average color.

    - __turnoff/turnon__: Controls the LED strip's power state.
# Usage

## 1. Upload the Arduino Sketch
- Open the [Arduino IDE](https://www.arduino.cc/en/software).

- Navigate to the arduino folder in this project and open the .ino file (e.g., LED_Control.ino).

- Connect your Arduino to your computer.

- Select the correct board and port from the Tools menu in the Arduino IDE.

- Upload the sketch to your Arduino.

## 2. Connect the Arduino
- Ensure your Arduino is connected to your computer and the correct port is detected by the application.

## 3. Run the Application
- Execute the 'Led Controller.exe' from **dist folder** to start the application:

## 4. Select a Color
- Use the color wheel to select a color. The selected color will be sent to the Arduino, and the LED strip will update accordingly.

## 5. Adjust Brightness
- Use the slider to adjust the brightness of the selected color.

## 6. Enable Modes
Toggle the switches to enable different lighting modes:

- Rainbow Mode: Cycles through a spectrum of colors.

- Pulsating Mode: Changes the LED color based on audio input (bass, mids, highs).

- Ambient Mode: Matches the LED color to the average color of your screen.

## 7. Turn On/Off
- Use the On/Off button to control the power state of the LED strip.

## 8. System Tray
- The application can be minimized to the system tray. Right-click the tray icon to restore the application or quit.

### Notes
- Ensure the Arduino is properly set up to receive RGB values via serial communication.

- The Pulsating mode requires an audio input device to be connected and configured.

- The Ambient mode captures the screen's average color and may require additional permissions on some operating systems.
# Pulsating Mode
#### VB-Cable Virtual Audio Cable
**Purpose**: VB-Cable is a virtual audio device that allows you to route audio from one application to another. It is useful for capturing audio input for the Pulsating Mode.

Download Link: [VB-Cable Virtual Audio Cable](https://vb-audio.com/Cable/)

__Installation:__

- Download the VB-Cable installer from the [official website](https://vb-audio.com/Cable/).

- Run the installer and follow the on-screen instructions.

- After installation, VB-Cable will appear as an audio device in your system's sound settings.

__Configuration:__

- Set VB-Cable as the default playback device in your system's sound settings.

- Set VB-Cable as the default recording device to capture the audio input for the Pulsating Mode.
# Hardware Requirements

- Arduino Uno 
- RGB LED strip (NON ADDRESABLE)
- USB cable for Arduino
- Jumper wires
- Power supply for the LED strip
## 🔗 Links

[Email](mailto:afsalshajibismi@gmail.com)

[Instagram](https:www.instagram.com/afsaldigitalart)

