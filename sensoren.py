import requests
import os
import time
import board
import adafruit_dht
import mh_z19

API_KEY = "2XS75TPDRDCAY6LP"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# Setze den seriellen Port für MH-Z19
os.environ["SERIALPORT"] = "/dev/serial0"

# Initialisiere DHT11 an GPIO17
dhtDevice = adafruit_dht.DHT11(board.D17)

print("Messung gestartet. Drücke Strg+C zum Beenden.")

try:
    while True:
        try:
            # Temperatur und Luftfeuchtigkeit vom DHT-Sensor
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity

            # CO2-Wert vom MH-Z19
            co2_data = mh_z19.read()
            co2 = co2_data.get("co2", None) if co2_data else None

            print(
                "Temp: {:.1f} °C    Feuchtigkeit: {}%    CO2: {} ppm".format(
                    temperature_c, humidity, co2
                )
            )

            if temperature_c is not None and humidity is not None and co2 is not None:
                # Daten an ThingSpeak senden
                payload = {
                    "api_key": API_KEY,
                    "field1": temperature_c,
                    "field2": humidity,
                    "field3": co2,
                }
                response = requests.get(THINGSPEAK_URL, params=payload)
                print(f"ThingSpeak Response: {response.text}")
            else:
                print("Ein oder mehrere Sensorwerte fehlen. Nichts gesendet.")

        except RuntimeError as error:
            # DHT-Sensorfehler sind normal – weiter machen
            print("Sensorfehler:", error.args[0])

        time.sleep(16)  # alle 60 Sekunden senden

except KeyboardInterrupt:
    print("\nMessung beendet durch Benutzer (Strg+C).")
finally:
    dhtDevice.exit()
