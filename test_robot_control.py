from math import radians, cos, acos, degrees
import matplotlib.pyplot as plt
import numpy as np

c = 1 # ค่าคงที่การเลี้ยว
l = 1 # ระยะห่างระหว่างล้อ
v = 1 # ความเร็วปกติ
pt = radians(90) # มุมที่ต้องการจะเป็น
p0 = radians(0) # มุมตอนเริ่มเลี้ยว

T = 2/c * acos(1 - c*l/(2*v)*(pt-p0)) # เวลาที่ใช้ในการเลี้ยว

def get_zeta(t):
    if (t <= T/2):
        return c*t
    return c*T-c*t

def get_p(t):
    if t <= T/2:
        return p0 + v/(c*l)*(1-cos(get_zeta(t))) + get_zeta(t)
    return p0 + v/(c*l)*(1-2*cos(c*T/2)+cos(get_zeta(t)))+get_zeta(t)

def for_each(lst, callback):
    data = []
    for i in lst:
        data.append(callback(i))
    return data

t = np.arange(0., T, T/100)
plt.plot(t, for_each(t, get_zeta), 'r--', t, for_each(t, get_p), 'b--')
plt.show()