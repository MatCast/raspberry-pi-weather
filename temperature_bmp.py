import bme280
import smbus2
from time import sleep

port = 1
address = 0x76
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus, address)


def read_all():
    bme280_data = bme280.sample(bus, address)
    data = {
        "temperature": bme280_data.temperature,
        "humidity": bme280_data.humidity,
        "pressure": bme280_data.pressure,
    }
    return data


def read_all_and_format():
    data = read_all()
    data_fmt = (
        f"Temperature: {data['temperature']:.2f} °C"
        f"\nHumidity: {data['humidity']:.2f} %"
        f"\nPressure: {data['pressure']:.2f} bar\n"
    )
    return data_fmt
