from temperature_bmp import read_all
import time

while True:
    print(read_all())
    time.sleep(1)