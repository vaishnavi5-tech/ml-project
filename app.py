from flask import Flask, jsonify, request, render_template
import joblib
import psutil
import serial
import time

# ─────────────────────────────
# CREATE FLASK APP
# ─────────────────────────────
app = Flask(__name__)

# ─────────────────────────────
# CONFIG
# ─────────────────────────────
SERIAL_PORT = "COM7"
BAUD_RATE = 9600
MODEL_PATH = "cooling.pkl"

# ─────────────────────────────
# LOAD MODEL
# ─────────────────────────────
model = joblib.load(MODEL_PATH)

# ─────────────────────────────
# CONNECT TO ARDUINO
# ─────────────────────────────
arduino = None

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
    time.sleep(2)

    print("✅ Arduino connected!")

except Exception as e:

    print("❌ Arduino connection failed:", e)

print("✅ Flask server started!")

# ─────────────────────────────
# HOME PAGE
# ─────────────────────────────
@app.route('/')
def home():
    return render_template('index.html')

# ─────────────────────────────
# SEND TO ARDUINO
# ─────────────────────────────
def send_to_arduino(heat):

    # OFF
    if heat < 30:

        status = "OFF"
        signal = '0'

    # LOW
    elif heat < 40:

        status = "LOW"
        signal = 'L'

    # MEDIUM
    elif heat <= 70:

        status = "MEDIUM"
        signal = 'M'

    # HIGH
    else:

        status = "HIGH"
        signal = 'H'

    print("Heat:", heat)
    print("Signal:", signal)

    if arduino:

        arduino.write(signal.encode())

    return status
# ─────────────────────────────
# GET REALTIME SYSTEM STATS
# ─────────────────────────────
def get_realtime_stats():

    cpu = psutil.cpu_percent(interval=1)

    ram = psutil.virtual_memory().percent

    disk = psutil.disk_usage('/').percent

    memory = ram

    power_cycles = 500

    return [disk, cpu, ram, memory, power_cycles]
# ─────────────────────────────
# CALCULATE HEAT / PWM / RPM
# ─────────────────────────────
def calculate_thermal(cpu, ram, disk):

    # Weighted heat score
    heat = (cpu * 0.4) + (ram * 0.3) + (disk * 0.3)

    # PWM calculation
    if heat < 30:
        pwm = 0
    elif heat <40:
        pwm=80
    elif heat <= 70:
        pwm = int(((heat - 40) / 30) * 150)

    else:
        pwm = 255

    # RPM simulation
    rpm = int((pwm / 255) * 3000)

    return round(heat, 1), pwm, rpm
# ─────────────────────────────
# REALTIME API
# ─────────────────────────────
@app.route('/realtime')

def realtime():

    stats = get_realtime_stats()

    cpu  = round(stats[1], 1)
    ram  = round(stats[2], 1)
    disk = round(stats[0], 1)

    heat, pwm, rpm = calculate_thermal(cpu, ram, disk)

    prediction = model.predict([stats])[0]

    status = send_to_arduino(heat)

    return jsonify({

        "cpu": cpu,
        "ram": ram,
        "disk": disk,
        "fan": status,
        "heat": heat,
        "pwm": pwm,
        "rpm": rpm

    })

# ─────────────────────────────
# MANUAL INPUT API
# ─────────────────────────────
@app.route('/manual', methods=['POST'])

def manual():

    data = request.get_json()

    cpu = float(data['cpu'])
    ram = float(data['ram'])
    disk = float(data['disk'])

    memory = ram
    power_cycles = 500

    stats = [disk, cpu, ram, memory, power_cycles]

    # Calculate heat/PWM/RPM
    heat, pwm, rpm = calculate_thermal(cpu, ram, disk)

    prediction = model.predict([stats])[0]

    status = send_to_arduino(heat)

    return jsonify({

        "cpu": cpu,
        "ram": ram,
        "disk": disk,
        "fan": status,
        "heat": heat,
        "pwm": pwm,
        "rpm": rpm

    })

# ─────────────────────────────
# RUN APP
# ─────────────────────────────
if __name__ == '__main__':

    app.run(debug=False)