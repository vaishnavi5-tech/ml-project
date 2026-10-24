import joblib
import psutil
import serial
import time

# ─── CONFIG ───────────────────────────────────────────────
SERIAL_PORT = "COM7"
BAUD_RATE   = 9600
MODEL_PATH  = "cooling.pkl"
# ──────────────────────────────────────────────────────────

# Load model and connect Arduino
model   = joblib.load(MODEL_PATH)
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)
print("✅ Model loaded!")
print(f"✅ Arduino connected on {SERIAL_PORT}\n")

# ─── GET REAL-TIME STATS (5 features) ─────────────────────
def get_realtime_stats():
    disk         = psutil.disk_usage('/').percent
    cpu          = psutil.cpu_percent(interval=1)
    ram          = psutil.virtual_memory().percent
    memory       = psutil.virtual_memory().percent
    power_cycles = 500

    return [disk, cpu, ram, memory, power_cycles]

# ─── GET MANUAL STATS (5 features) ────────────────────────
def get_manual_stats():
    print("\n  Enter values  |  Type 'back' to return to menu\n")
    try:
        inputs = []
        prompts = [
            "  Disk Usage     (0-100)  : ",
            "  CPU Usage      (0-100)  : ",
            "  RAM Usage      (0-100)  : ",
            "  Memory Usage   (0-100)  : ",
            "  Power Cycles   (0-1000) : "
        ]
        for p in prompts:
            val = input(p).strip()
            if val.lower() == 'back':
                return None
            inputs.append(float(val))

        return inputs

    except ValueError:
        print("\n  ❌ Invalid input! Numbers only.\n")
        return None

# ─── SEND TO ARDUINO ───────────────────────────────────────
def send_to_arduino(prediction):
    match prediction:
        case 1:
            arduino.write(b'1')
            print("  🔴 Prediction → Fan ON  | LED ON")
        case 0:
            arduino.write(b'0')
            print("  🟢 Prediction → Fan OFF | LED OFF")
        case _:
            print("  ⚠️ Unknown prediction value")

# ─── SHOW MENU ─────────────────────────────────────────────
def show_menu():
    print("\n" + "=" * 40)
    print("     SMART COOLING SYSTEM CONTROLLER")
    print("=" * 40)
    print("   R  →  Real-time mode (auto)")
    print("   M  →  Manual  mode  (type values)")
    print("   Q  →  Quit")
    print("=" * 40)

# ─── MAIN LOOP ─────────────────────────────────────────────
try:
    while True:
        show_menu()
        choice = input("\n  Select mode (R / M / Q): ").strip().upper()

        match choice:

            # ── REAL-TIME MODE ──────────────────────────
            case 'R':
                print("\n  🔁 Real-time mode started.")
                print("  Press Enter each cycle | Type 'B' to go back\n")

                while True:
                    stats = get_realtime_stats()
                    print(f"\n  📊 Disk:{stats[0]}%  CPU:{stats[1]}%  "
                          f"RAM:{stats[2]}%  Mem:{stats[3]}%  "
                          f"Power:{stats[4]}")

                    prediction = model.predict([stats])[0]
                    send_to_arduino(prediction)

                    time.sleep(2)
                    go = input("\n  Enter → next reading | B → back to menu : ").strip().upper()
                    if go == 'B':
                        print("\n  ↩️  Returning to menu...")
                        break

            # ── MANUAL MODE ─────────────────────────────
            case 'M':
                print("\n  ✏️  Manual mode started.")

                while True:
                    stats = get_manual_stats()

                    if stats is None:
                        print("\n  ↩️  Returning to menu...")
                        break

                    print(f"\n  📊 Input : {stats}")
                    prediction = model.predict([stats])[0]
                    send_to_arduino(prediction)

                    again = input("\n  Test again? (Y → yes | B → back to menu) : ").strip().upper()
                    if again != 'Y':
                        print("\n  ↩️  Returning to menu...")
                        break

            # ── QUIT ────────────────────────────────────
            case 'Q':
                arduino.write(b'0')
                arduino.close()
                print("\n  🛑 Exiting... LED turned OFF. Goodbye!\n")
                break

            # ── INVALID ─────────────────────────────────
            case _:
                print("\n  ❌ Invalid choice! Enter R, M, or Q only.")

except KeyboardInterrupt:
    arduino.write(b'0')
    arduino.close()
    print("\n\n  🛑 Force stopped. LED turned OFF.\n")