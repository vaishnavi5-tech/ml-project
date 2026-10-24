# ml-project
Arduino-based adaptive cooling system using dual DHT11 sensors, PWM fan control via L298N, and a 16×2 LCD. Built with Arduino C++ and Proteus, with Python dashboard integration and planned ML-based optimization and cloud monitoring.
# 🌡️ Smart Thermal AI — Adaptive Cooling System

A Python and Arduino-based smart cooling project that combines system-resource monitoring, a machine-learning model, a Flask web dashboard, and serial communication with an Arduino. The dashboard calculates a weighted heat score from CPU, RAM, and disk usage and uses it to determine a cooling status.

The repository also includes Arduino firmware for dual-DHT11 temperature monitoring, LCD display, and threshold-based PWM fan control.

## 📸 Project Preview

### Smart Thermal AI Dashboard

<img width="946" height="424" alt="image" src="https://github.com/user-attachments/assets/4012ab98-fefc-4fb5-ad17-361421580861" />


### Proteus Circuit Simulation

<img width="1770" height="874" alt="image" src="https://github.com/user-attachments/assets/4fb4d1b1-11ca-4a7f-80d2-f30366fb2869" />


## ✨ Features

- 📊 Real-time CPU, RAM, and disk-usage monitoring.
- 🧠 Loads a saved machine-learning model using Joblib.
- 🌡️ Calculates a weighted heat score from system-resource metrics.
- 🌬️ Determines cooling status and calculates a PWM value.
- 💻 Flask-based web dashboard with real-time and manual modes.
- 🔌 Serial communication between Python and Arduino.
- 📟 Arduino firmware for two DHT11 sensors and a 16×2 LCD.
- ⚙️ Temperature-based PWM control logic for two fan channels.
- 🧪 Proteus circuit simulation support.

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend logic and system monitoring |
| Flask | Web application and API endpoints |
| scikit-learn-compatible model loading | Machine-learning inference through Joblib |
| psutil | CPU, RAM, and disk monitoring |
| PySerial | Serial communication with Arduino |
| HTML, CSS, JavaScript | Dashboard interface |
| Arduino C++ | Sensor reading, LCD display, and fan control |
| DHT11 | Temperature and humidity sensing |
| L298N motor driver | Planned dual DC motor control |
| Proteus | Circuit simulation |

## 🏗️ Project Structure

```text
Python-Aurdino-main/
├── app.py
├── temp_monitor.py
├── 111.py
├── cooling.pkl
├── templates/
│   └── index.html
├── images/
│   ├── dashboard.png
│   └── proteus-circuit.png
└── README.md
```

The `images/` directory is for screenshots you add; it is not included in the original project ZIP.

## 🔄 How It Works

### Python Dashboard

1. Collects CPU, RAM, and disk-usage statistics using `psutil`.
2. Calculates the weighted heat score:

   `Heat Score = (CPU × 0.4) + (RAM × 0.3) + (Disk × 0.3)`

3. Calculates a PWM value and an estimated fan RPM for dashboard display.
4. Loads `cooling.pkl` and calls the model's prediction method.
5. Sends a cooling-status character to the Arduino over serial communication.
6. Displays the collected statistics and calculated values on the Flask dashboard.

### Arduino Temperature Controller

The separate Arduino firmware reads two DHT11 sensors, displays readings on a 16×2 LCD, and uses temperature thresholds to control two PWM motor channels.

**Note:** The Python dashboard and Arduino temperature-control sketch use different input signals and control logic in the supplied code. Their complete integration into a single ML-based temperature controller remains a development task.

## 🖥️ Getting Started

### 1. Requirements

- Python installed on your computer
- Arduino IDE, if using the Arduino firmware
- Arduino board and appropriate serial connection, when available
- The `cooling.pkl` model file
- The required Python packages

### 2. Install Python Dependencies

Open a terminal in the project directory and run:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

Install the packages:

```bash
pip install Flask joblib psutil pyserial scikit-learn
```

Use a compatible scikit-learn version for the environment in which `cooling.pkl` was created.

### 3. Configure the Serial Port

The current Python files specify:

```python
SERIAL_PORT = "COM7"
BAUD_RATE = 9600
```

Change `COM7` to the port assigned to your Arduino. Ensure the Arduino firmware uses a compatible baud rate and the serial messages expected by the Python application.

### 4. Run the Flask Dashboard

From the project directory:

```bash
python app.py
```

Open the local address shown by Flask in your browser. By default, Flask typically uses:

`http://127.0.0.1:5000`

The dashboard uses these endpoints:

- `GET /` — dashboard page
- `GET /realtime` — retrieves system statistics and calculated cooling values
- `POST /manual` — processes manually supplied CPU, RAM, and disk values

### 5. Run the Command-Line Monitor (Optional)

The repository also includes a separate monitoring script:

```bash
python temp_monitor.py
```

This script loads the saved model and provides real-time and manual modes. It attempts to connect to the configured Arduino serial port.

**Important:** Do not run multiple scripts that open the same serial port simultaneously.

## 📈 Heat Score and Cooling Status

The Flask backend calculates the weighted heat score using CPU, RAM, and disk utilization.

| Heat score | Dashboard status / serial signal |
|---|---|
| Below 30 | OFF — `0` |
| 30 to below 40 | LOW — `L` |
| 40 to 70 | MEDIUM — `M` |
| Above 70 | HIGH — `H` |

The dashboard also calculates a PWM value between 0 and 255 and estimates fan RPM mathematically. These values are calculated or simulated by the current software; they should not be treated as measured physical fan speed.

## 🔌 Arduino Pin Mapping

The Arduino sketch uses the following assignments:

| Component | Arduino pin |
|---|---|
| DHT11 sensor 1 data | A0 |
| DHT11 sensor 2 data | A1 |
| LCD RS | D7 |
| LCD Enable | D8 |
| LCD D4 | D4 |
| LCD D5 | D3 |
| LCD D6 | D2 |
| LCD D7 | D13 |
| L298N ENA (PWM) | D6 |
| L298N IN1 / IN2 | D12 / D11 |
| L298N ENB (PWM) | D5 |
| L298N IN3 / IN4 | D10 / D9 |

Verify the wiring, motor supply, and common ground before connecting physical hardware.

## 🧪 Current Development Status

- [x] Flask dashboard interface
- [x] CPU, RAM, and disk monitoring
- [x] Weighted heat-score calculation
- [x] Saved model loading and prediction calls
- [x] Manual and real-time dashboard endpoints
- [x] Arduino temperature-control sketch
- [ ] Verify the complete Python-to-Arduino integration
- [ ] Validate the model with documented test data
- [ ] Test physical fan operation and measure actual RPM
- [ ] Evaluate cooling effectiveness and power consumption
- [ ] Deploy an optional cloud-hosted dashboard

## 🔮 Future Improvements

- Integrate temperature readings into the ML decision pipeline.
- Validate the model and document its training dataset and metrics.
- Improve fault handling for sensor and serial-connection errors.
- Add historical logging and temperature trend analysis.
- Add secure remote monitoring through an optional server.
- Compare adaptive cooling against a conventional threshold-based baseline.

## 👩‍💻 Author

**Vaishnavi M**

Computer Science and Engineering — Artificial Intelligence and Machine Learning

## 📄 License

A license has not yet been specified. Add a `LICENSE` file if you intend to distribute the project under an open-source license.
