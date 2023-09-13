import serial
import time
import matplotlib.pyplot as plt
import base64
import uuid

ser=serial.Serial("/dev/ttyACM0",9600) 
img_name = uuid.uuid1() 

ecg = []
x = []
y = []
count = 0

time.sleep(5)

while True:
    ser.write("1".encode('utf-8'))
    read_ser = ser.readline().decode('utf-8').rstrip()

    if read_ser != "": 
        count += 1

    if count >= 500:
        fig = plt.get_current_fig_manager()
        fig.full_screen_toggle()
        fig = plt.gcf()
        fig.set_size_inches(15.5, 8.5)

    for a in range(len(ecg)):
        x.append(a)

        plt.plot(x, ecg)
        plt.xlabel('Time (ms)')
        plt.ylabel('Signal (mV)')
        plt.savefig(f'{img_name}.jpg', format='jpg', dpi=50)

        plt.show(block=False)
        plt.waitforbuttonpress(5)
        plt.close('all')

        with open(f'{img_name}.jpg', "rb") as img_file: 
            b64_string = base64.b64encode(img_file.read())
            b64_string = b64_string.decode('utf-8')
            print(str(b64_string.replace(" ", "+")))
            break

    ecg.append(int(read_ser))