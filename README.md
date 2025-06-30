# Smart Home Automation & Alert System

A comprehensive IoT-based smart home automation system using MicroPython, featuring multiple sensors, cloud connectivity, and real-time monitoring capabilities.

## 🏠 Features

- **Multi-Sensor Monitoring**
  - DHT11 Temperature & Humidity sensor
  - Flame detection with LED alert
  - Gas leak detection with buzzer alarm
  - PIR motion detection with LED indicator

- **Remote Control & Monitoring**
  - Blynk app integration for remote LED control
  - Real-time sensor data display on Blynk dashboard
  - ThingSpeak cloud logging for data analytics

- **Alert Systems**
  - Visual alerts using LEDs for different events
  - Audio alerts using buzzer for gas emergencies
  - Real-time notifications through Blynk app

## 🛠️ Hardware Requirements

### Microcontroller
- ESP32 or ESP8266 (MicroPython compatible)

### Sensors & Components
| Component | Pin | Purpose |
|-----------|-----|---------|
| DHT11 | Pin 10 | Temperature & Humidity |
| Flame Sensor | Pin 16 | Fire detection |
| PIR Sensor | Pin 15 | Motion detection |
| Gas Sensor (MQ-2) | Pin 26 (ADC) | Gas leak detection |
| LED 1 | Pin 11 | Blynk controlled |
| LED 2 | Pin 4 | Motion indicator |
| LED 3 | Pin 3 | Flame alert |
| Buzzer | Pin 13 | Gas alarm |

## 📋 Prerequisites

### Software Requirements
- MicroPython firmware installed on your microcontroller
- Blynk mobile app
- ThingSpeak account

### Required Libraries
- `BlynkLib` (included in repository)
- `urequests` (built-in MicroPython)
- `network` (built-in MicroPython)
- `machine` (built-in MicroPython)
- `dht` (built-in MicroPython)

## 🚀 Installation & Setup

### 1. Hardware Setup
1. Connect all sensors and components according to the pin configuration
2. Ensure proper power supply (3.3V/5V as required)
3. Flash MicroPython firmware to your microcontroller

### 2. Software Configuration

1. **Clone this repository:**
   ```bash
   git clone https://github.com/avimanna/Smart-Home-Automation-and-Alert-System.git
   cd smart-home-automation
   ```

2. **Upload files to your microcontroller:**
   - `main.py` (the main system script)
   - `BlynkLib.py`

3. **Configure credentials in `main.py`:**
   ```python
   # Wi-Fi credentials
   WIFI_SSID = 'your_wifi_name'
   WIFI_PASSWORD = 'your_wifi_password'
   
   # Blynk Authentication Token
   BLYNK_AUTH = 'your_blynk_auth_token'
   
   # ThingSpeak Write API Key
   THINGSPEAK_API_KEY = 'your_thingspeak_api_key'
   ```

### 3. Blynk App Setup

1. Install Blynk app on your smartphone
2. Create a new project and select your device type
3. Add the following widgets:
   - **Button** → Virtual Pin V0 (LED Control)
   - **Value Display** → Virtual Pin V1 (Temperature)
   - **Value Display** → Virtual Pin V2 (Humidity)
   - **Gauge** → Virtual Pin V3 (Gas Level)
   - **LED** → Virtual Pin V4 (Flame Status)
   - **LED** → Virtual Pin V5 (Motion Status)

### 4. ThingSpeak Setup

1. Create a ThingSpeak account at [thingspeak.com](https://thingspeak.com)
2. Create a new channel with the following fields:
   - Field 1: Temperature
   - Field 2: Humidity
   - Field 3: Gas Level
   - Field 4: Flame Detection
   - Field 5: Motion Detection
3. Copy your Write API Key

## 📱 Usage

1. Power on your device
2. The system will automatically connect to Wi-Fi
3. Monitor sensor data through:
   - Serial console output
   - Blynk mobile app
   - ThingSpeak dashboard
4. Control LED remotely using Blynk app
5. Receive alerts for:
   - Fire detection (LED + Blynk notification)
   - Gas leaks (Buzzer + Blynk notification)
   - Motion detection (LED + Blynk notification)

## 📊 Monitoring & Analytics

### Real-time Monitoring
- **Blynk Dashboard**: Live sensor readings and control
- **Serial Output**: Console logging for debugging

### Data Analytics
- **ThingSpeak**: Historical data, charts, and analytics
- **Data Export**: CSV export available from ThingSpeak

## 🔧 Customization

### Adding New Sensors
1. Define new pin in the hardware configuration section
2. Create sensor reading function
3. Add to main loop with appropriate timing
4. Update Blynk and ThingSpeak integration

### Modifying Alert Thresholds
```python
# Gas sensor threshold (adjust as needed)
if gas_value >= 15000:  # Change this value
    print("DANGER!! Gas levels too high!")
```

### Changing Update Intervals
```python
THINGSPEAK_INTERVAL = 15  # seconds between ThingSpeak updates
SENSOR_CHECK_INTERVAL = 2  # seconds between sensor checks
```

## 🐛 Troubleshooting

### Common Issues

**Wi-Fi Connection Problems:**
- Verify SSID and password
- Check signal strength
- Ensure 2.4GHz network (ESP8266 doesn't support 5GHz)

**Sensor Reading Errors:**
- Check wiring connections
- Verify power supply voltage
- Ensure proper pull-up/pull-down resistors

**Blynk Connection Issues:**
- Verify auth token
- Check internet connectivity
- Ensure Blynk server is accessible

**ThingSpeak Upload Failures:**
- Verify API key
- Check update interval (minimum 15 seconds)
- Ensure internet connectivity

## 📈 Future Enhancements

- [ ] Add more sensor types (smoke, sound, light)
- [ ] Implement local data storage
- [ ] Add web interface for configuration
- [ ] Include email/SMS notifications
- [ ] Add scheduling and automation rules
- [ ] Implement OTA (Over-The-Air) updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-sensor`)
3. Commit your changes (`git commit -am 'Add new sensor support'`)
4. Push to the branch (`git push origin feature/new-sensor`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@avimanna](https://github.com/avimanna)
- Email: dev.avijitmanna@gmail.com

## 🙏 Acknowledgments

- Blynk team for the excellent IoT platform
- MicroPython community for the amazing firmware
- ThingSpeak for data analytics platform

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/avimanna/Smart-Home-Automation-and-Alert-System/issues) page
2. Create a new issue with detailed description
3. Join our [Discussions](https://github.com/avimanna/Smart-Home-Automation-and-Alert-System/discussions) for community support

---

⭐ **Star this repository if you found it helpful!**
