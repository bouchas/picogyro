import machine
import math
import mpu6050
import utime

sda=machine.Pin(8)
scl=machine.Pin(9)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=400000)

print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))

for device in devices:
  print("Decimal address: ",device," | Hexa address: ",hex(device))

mpu = mpu6050.MPU6050()
mpu.setSampleRate(200)
mpu.setGResolution(2)

def averageMPU( count, timing_ms):
    gx = 0
    gy = 0
    gz = 0
    gt = 0
    gxoffset =  0.07
    gyoffset = -0.04
    for i in range(count):
        g=mpu.readData()
        # offset mpu
        gx = gx + g.Gx - gxoffset
        gy = gy + g.Gy - gyoffset
        gz = gz + g.Gz
        gt = gt + g.Temperature
        
        utime.sleep_ms(timing_ms)
    return gx/count, gy/count, gz/count, gt/count

while True:
    gx, gy, gz, gt = averageMPU(20,5)
    print("X:{:.2f}  Y:{:.2f}  Z:{:.2f}  T:{:.2f}".format(gx,gy,gz,gt))

    ## calculate vector dimension
    #vdim = math.sqrt( gx*gx + gy*gy + gz*gz)
           
    ## get x angle
    #rad2degree= 180 / math.pi
    #angleX =  rad2degree * math.asin(gx / vdim)
    #angleY =  rad2degree * math.asin(gy / vdim)

