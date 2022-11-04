import bme280
import smbus2
from datetime import datetime
import pytz
import time

port = 1
address = 0x76
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus, address)


def read_all():
    bme280_data = bme280.sample(bus, address)
    reading_date = datetime.utcnow()
    data = {
        "timestamp": reading_date,
        "temperature": bme280_data.temperature,
        "humidity": bme280_data.humidity,
        "pressure": bme280_data.pressure,
    }
    return data


def read_multiple_times(secs=1, n_readings=5):
    data_list = []
    for i in range(n_readings):
        data_list.append(read_all())
        time.sleep(secs)
    return data_list


def average(lst):
    return sum(lst) / len(lst)


def time_avg(lst):
    return lst[0] + (lst[-1] - lst[0]) / 2


def dict_to_long(data_list):
    long_dict = {k: [v] for k, v in data_list[0].items()}
    if len(data_list) > 1:
        for data in data_list[1:]:
            for k, v in data.items():
                long_dict[k].append(v)
    return long_dict


def get_avg(data_list):
    long_dict = dict_to_long(data_list)
    avg_data = {}
    for k, v in long_dict.items():
        try:
            avg_data[k] = average(v)
        except TypeError:
            avg_data[k] = time_avg(v)
    return avg_data


def format_readings(data):
    timestamp = data["timestamp"]
    reading_time = (
        pytz.utc.localize(timestamp).astimezone().strftime("%Y-%m-%d, %H:%M:%S")
    )
    data_fmt = (
        f"{reading_time}"
        f"\nTemperature: {data['temperature']:.2f} °C"
        f"\nHumidity: {data['humidity']:.2f} %"
        f"\nPressure: {data['pressure']:.2f} bar"
    )
    return data_fmt


def read_all_and_format():
    data = read_all()
    return format_readings(data)


if __name__ == "__main__":

    data_list = []
    for i in range(1):
        data = {
            "timestamp": datetime.utcnow(),
            "temperature": 12 + i,
            "humidity": 67 + i,
            "pressure": 980 + i,
        }
        data_list.append(data)
    print(get_avg(data_list))
