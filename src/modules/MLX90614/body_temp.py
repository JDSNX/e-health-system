from mlx90614 import MLX90614
from smbus2 import SMBus

bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
print(sensor.get_obj_temp())
bus.close()
