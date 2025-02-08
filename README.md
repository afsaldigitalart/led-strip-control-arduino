# LED Strip Control Software

## Strictly personal program for my Personal Computer. For personal learning purpose only

This software provides an interactive graphical user interface (GUI) to control an RGB LED strip using an Arduino. It allows users to select colors, adjust brightness, enable dynamic lighting effects (rainbow mode, pulsating mode), and sync LED brightness with audio levels.

## Features

- 🎨 **Color Selection**: Pick colors from a color wheel.
- 🔆 **Brightness Control**: Adjust LED brightness via a slider.
- 🌈 **Rainbow Mode**: Smoothly transitions colors.
- 💡 **Pulsating Mode**: Syncs LED brightness with audio.
- 🖥️ **System Tray Support**: Runs in the background when minimized.
- 🔌 **Automatic Arduino Port Detection**: Identifies connected Arduino automatically.

## Installation

### Prerequisites
- **Python 3.x**
- Install dependencies using:

  ```sh
  pip install -r requirements.txt

- Install ([VB Cable Virtual Audio](https://vb-audio.com/Cable/)) for the working of Pulsating Mode
After turning on Pulsing mode, change the output device to VB Virtual Audio (Change output only after turning on the Pulsating Mode) 


## Running the Application

1. **Connect the Arduino** with the LED strip.
2. **Upload the corresponding Arduino sketch** (if required).
3. **Run the script** using:

   ```sh
   python main.py

#### Or run the .exe file inside dist folder


## Usage

### 🎨 Select a Color
- Click on the **color wheel** to set the LED color.

### 🔆 Adjust Brightness
- Use the **brightness slider** to control LED brightness.

### 🌈 Enable Effects
- Toggle **Rainbow Mode** for smooth color cycling.
- Toggle **Pulsating Mode** to sync LED brightness with audio.

### 💡 Turn ON/OFF
- Click the **power button** to switch the LED strip on or off.

### 🖥️ Minimize to Tray
- The app **runs in the background** when minimized.

## Technologies Used

- 🐍 **Python** – Core programming language
- 🎨 **CustomTkinter** – For the graphical user interface
- 🔌 **PySerial** – For communication with Arduino
- 🖼️ **Pillow** – For image processing (color wheel)
- 🖥️ **PyStray** – For system tray integration
- 🎵 **Sounddevice & NumPy** – For audio processing

## Future Enhancements

- 🎵 **Improved Audio Spectrum Analysis** – More accurate LED sync.
- 🕹️ **Mobile App Integration** – Remote control via a smartphone.
- 🧩 **Custom LED Animations** – More dynamic lighting effects.
