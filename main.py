from time import sleep
import time
import network
from machine import Pin, ADC
import BlynkLib
import urequests
from dht import DHT11
from DHT11 import InvalidChecksum


# Wi-Fi credentials
WIFI_SSID = 'ENTER_YOUR_SSID_HERE'
WIFI_PASSWORD = 'ENTER_YOUR_PASSWORD_HERE'

# Blynk Authentication Token
BLYNK_AUTH = 'ENTER_YOUR_BLYNK_AUTH_TOKEN_HERE'

# ThingSpeak Write API Key
THINGSPEAK_API_KEY = 'ENTER_YOUR_API_KEY_HERE'


# LEDs
led1 = Pin(11, Pin.OUT)  # Blynk controlled LED
led2 = Pin(4, Pin.OUT)   # Motion detection LED
led3 = Pin(3, Pin.OUT)   # Flame detection LED

# Sensors
dht_pin = Pin(10, Pin.OUT, Pin.PULL_DOWN)  # DHT11 sensor
flame_sensor = Pin(16, Pin.IN)             # Flame sensor
pir_sensor = Pin(15, Pin.IN)               # PIR motion sensor
gas_sensor = ADC(Pin(26))                  # Gas sensor (analog)

# Actuators
buzzer = Pin(13, Pin.OUT)                  # Gas alert buzzer


# Initialize sensors
dht_sensor = DHT11(dht_pin)

# Timing variables
last_thingspeak_update = 0
last_sensor_check = 0
last_motion_check = 0
THINGSPEAK_INTERVAL = 15  # seconds
SENSOR_CHECK_INTERVAL = 2  # seconds
MOTION_CHECK_INTERVAL = 1  # seconds

# System status
temperature = 0
humidity = 0
gas_level = 0
flame_detected = False
motion_detected = False

# HTTP headers for ThingSpeak
HTTP_HEADERS = {'Content-Type': 'application/json'}


def connect_to_wifi():
    """Connect to Wi-Fi network"""
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    
    if not sta_if.isconnected():
        print('Connecting to Wi-Fi...')
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            print('.', end='')
            time.sleep(1)
    
    print('\nWi-Fi Connected! Network config:', sta_if.ifconfig())
    return sta_if.isconnected()


def read_dht11():
    """Read temperature and humidity from DHT11 sensor"""
    global temperature, humidity
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        print(f"Temperature: {temperature}°C, Humidity: {humidity}%")
        return True
    except Exception as e:
        print(f"DHT11 reading error: {e}")
        return False

def check_flame():
    """Check for flame detection"""
    global flame_detected
    if flame_sensor.value() == 0:  # Active low sensor
        flame_detected = True
        led3.on()
        print("** FIRE DETECTED!!! **")
    else:
        flame_detected = False
        led3.off()

def check_gas():
    """Check gas levels and activate buzzer if dangerous"""
    global gas_level
    gas_value = gas_sensor.read_u16()
    voltage = gas_value * 3.3 / 65535
    gas_level = gas_value
    
    print(f"Gas Sensor - Value: {gas_value}, Voltage: {voltage:.2f}V")
    
    if gas_value >= 15000:
        print("DANGER!! Gas levels too high!")
        buzz_alert(0.5)
        return True
    else:
        print("Gas levels normal")
        return False

def check_motion():
    """Check for motion detection"""
    global motion_detected
    if pir_sensor.value() == 1:
        motion_detected = True
        led2.on()
        print("Motion detected!")
    else:
        motion_detected = False
        led2.off()

def buzz_alert(duration):
    """Activate buzzer for specified duration"""
    buzzer.value(1)
    time.sleep(duration)
    buzzer.value(0)
    time.sleep(duration)


def send_to_thingspeak():
    """Send sensor data to ThingSpeak"""
    try:
        # Prepare data payload
        data = {
            'field1': temperature,
            'field2': humidity,
            'field3': gas_level,
            'field4': 1 if flame_detected else 0,
            'field5': 1 if motion_detected else 0
        }
        
        url = f"http://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}"
        response = urequests.post(url, json=data, headers=HTTP_HEADERS)
        response.close()
        
        print(f"Data sent to ThingSpeak: {data}")
        return True
    except Exception as e:
        print(f"ThingSpeak upload error: {e}")
        return False


# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

@blynk.on("V0")
def v0_write_handler(value):
    """Handle Blynk virtual pin V0 for LED control"""
    if int(value[0]) == 1:
        led1.value(1)
        print("Blynk LED ON")
    else:
        led1.value(0)
        print("Blynk LED OFF")

@blynk.on("connected")
def blynk_connected():
    print("Blynk connected successfully!")
    # Send current sensor readings to Blynk
    blynk.virtual_write(1, temperature)  # V1 for temperature
    blynk.virtual_write(2, humidity)     # V2 for humidity
    blynk.virtual_write(3, gas_level)    # V3 for gas level
    blynk.virtual_write(4, 1 if flame_detected else 0)  # V4 for flame status
    blynk.virtual_write(5, 1 if motion_detected else 0) # V5 for motion status

def update_blynk_dashboard():
    """Update Blynk dashboard with current sensor readings"""
    try:
        blynk.virtual_write(1, temperature)
        blynk.virtual_write(2, humidity)
        blynk.virtual_write(3, gas_level)
        blynk.virtual_write(4, 1 if flame_detected else 0)
        blynk.virtual_write(5, 1 if motion_detected else 0)
    except Exception as e:
        print(f"Blynk update error: {e}")

def system_status_report():
    """Print comprehensive system status"""
    print("\n" + "="*50)
    print("SMART HOME SYSTEM STATUS")
    print("="*50)
    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")
    print(f"Gas Level: {gas_level}")
    print(f"Flame Status: {'DETECTED' if flame_detected else 'Normal'}")
    print(f"Motion Status: {'DETECTED' if motion_detected else 'No Motion'}")
    print(f"LED1 (Blynk): {'ON' if led1.value() else 'OFF'}")
    print(f"LED2 (Motion): {'ON' if led2.value() else 'OFF'}")
    print(f"LED3 (Flame): {'ON' if led3.value() else 'OFF'}")
    print("="*50 + "\n")

def initialize_system():
    """Initialize all system components"""
    print("Initializing Smart Home Automation System...")
    
    # Connect to Wi-Fi
    if not connect_to_wifi():
        print("Failed to connect to Wi-Fi!")
        return False
    
    # Test all components
    print("Testing sensors...")
    read_dht11()
    check_flame()
    check_gas()
    check_motion()
    
    print("System initialization complete!")
    system_status_report()
    return True

def main_loop():
    """Main system loop"""
    global last_thingspeak_update, last_sensor_check, last_motion_check
    
    current_time = time.time()
    
    # Handle Blynk communication
    blynk.run()
    
    # Check sensors at regular intervals
    if current_time - last_sensor_check >= SENSOR_CHECK_INTERVAL:
        read_dht11()
        check_flame()
        check_gas()
        last_sensor_check = current_time
        
        # Update Blynk dashboard
        update_blynk_dashboard()
    
    # Check motion more frequently
    if current_time - last_motion_check >= MOTION_CHECK_INTERVAL:
        check_motion()
        last_motion_check = current_time
    
    # Send data to ThingSpeak at specified intervals
    if current_time - last_thingspeak_update >= THINGSPEAK_INTERVAL:
        send_to_thingspeak()
        last_thingspeak_update = current_time
        system_status_report()


def main():
    """Main function to run the smart home system"""
    try:
        # Initialize system
        if not initialize_system():
            return
        
        print("Starting main system loop...")
        print("Press Ctrl+C to stop the system")
        
        # Main execution loop
        while True:
            main_loop()
            time.sleep(0.1)  # Small delay to prevent overwhelming the system
            
    except KeyboardInterrupt:
        print("\nSystem shutdown requested...")
        # Turn off all LEDs and buzzer
        led1.off()
        led2.off()
        led3.off()
        buzzer.off()
        print("Smart Home System stopped safely.")
    
    except Exception as e:
        print(f"System error: {e}")
        # Emergency shutdown
        led1.off()
        led2.off()
        led3.off()
        buzzer.off()

# Run the system
if __name__ == "__main__":
    main()