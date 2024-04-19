from struct import *
import socket
import sys, getopt, time, glob
import numpy as np
import pandas as pd
import nidaqmx
import matplotlib.pyplot as plt
import time
import csv
import torch
import torch.nn as nn

model = torch.load('model_epoch_100_v2.pth', map_location=torch.device('cpu'))

# 그래프 초기 설정
plt.ion()

fig = plt.figure()     #figure(도표) 생성

# ax = plt.subplot(311)
# ax2 = plt.subplot(312)
# ax3 = plt.subplot(313)
ax4 = plt.subplot(311)
ax5 = plt.subplot(312)
ax6 = plt.subplot(313)

x_data = []
y1_data = []
y2_data = []
y3_data = []
y4_data = []
y5_data = []
y6_data = []

y1_pred = []
y2_pred = []
y3_pred = []
y4_pred = []
y5_pred = []
y6_pred = []


s1_data = []
s2_data = []
s3_data = []
s4_data = []
s5_data = []
s6_data = []

data = bytearray(36)
Fx_ = bytearray(4)
Fy_ = bytearray(4)
Fz_ = bytearray(4)
Tx_ = bytearray(4)
Ty_ = bytearray(4)
Tz_ = bytearray(4)

Sensor_data = np.zeros([1,6])

Cal_FT = np.zeros([1,6])
Cal_St = np.zeros([1,6])
Real_St = np.zeros([1,6])

# ATI start command: 0x0002
# ATI stop command: 0x0000
start_command = str(chr(18))+str(chr(52))+str(chr(00))+str(chr(2))+str(chr(00))+str(chr(00))+str(chr(00))+str(chr(00))
stop_command = str(chr(18))+str(chr(52))+str(chr(00))+str(chr(00))+str(chr(00))+str(chr(00))+str(chr(00))+str(chr(1))
start_command = start_command.encode('utf-8')
stop_command = stop_command.encode('utf-8')
atiAddress = ('192.168.1.1',49152)

client = '192.168.1.100'

Strain_data = np.zeros([1,6])

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.connect(atiAddress)

serverSocket.sendto(start_command,atiAddress)
timeOffset = time.time();
j=1
while True:
    d = serverSocket.recvfrom_into(data, 36)
    for i in range(4):
        Fx_[i] = data[12 + i]
        Fy_[i] = data[16 + i]
        Fz_[i] = data[20 + i]
        Tx_[i] = data[24 + i]
        Ty_[i] = data[28 + i]
        Tz_[i] = data[32 + i]
    Fx = unpack('!i', Fx_)
    Fy = unpack('!i', Fy_)
    Fz = unpack('!i', Fz_)
    Tx = unpack('!i', Tx_)
    Ty = unpack('!i', Ty_)
    Tz = unpack('!i', Tz_)
    j=j+1
    if (j == 50):
        Cal_FT = np.array([[-Fy[0] / float(1000000), -Fx[0] / float(1000000),
                             Fz[0] / float(1000000), -Ty[0] / float(1000000),
                            -Tx[0] / float(1000000), Tz[0] / float(1000000)]])
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Dev1/ai1:6")
            Cal_St = task.read()
    if (j%150 == 0):
        x = time.time()
        print(Fx[0] / float(1000000), Fy[0] / float(1000000), Fz[0] / float(1000000), Tx[0] / float(1000000), Ty[0] / float(1000000), Tz[0] / float(1000000))
        Sensor_data = np.concatenate((Sensor_data, np.array([[-Fy[0] / float(1000000), -Fx[0] / float(1000000),
                                                              Fz[0] / float(1000000), -Ty[0] / float(1000000),
                                                              -Tx[0] / float(1000000), Tz[0] / float(1000000)]])-Cal_FT),
                                                            axis=0)

        x_data.append(x)
        y1_data.append(-Fy[0] / float(1000000)-Cal_FT[0][0])
        y2_data.append(-Fx[0] / float(1000000)-Cal_FT[0][1])
        y3_data.append(Fz[0] / float(1000000)-Cal_FT[0][2])
        y4_data.append(20*((-Ty[0] / float(1000000)-Cal_FT[0][3])+0.079*(-Fx[0] / float(1000000)-Cal_FT[0][1])))
        y5_data.append(20*((-Tx[0] / float(1000000)-Cal_FT[0][4])-0.079*(-Fy[0] / float(1000000)-Cal_FT[0][0])))
        y6_data.append(20*(Tz[0] / float(1000000)-Cal_FT[0][5]))
        # 그래프 업데이트
        # ax.clear()
        # ax2.clear()
        # ax3.clear()
        ax4.clear()
        ax5.clear()
        ax6.clear()
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Dev1/ai1:6")
            Real_St = task.read()
            s1 = (Real_St[0]-Cal_St[0])/1.5
            s2 = (Real_St[1]-Cal_St[1])/1.5
            s3 = (Real_St[2]-Cal_St[2])/1.5
            s4 = (Real_St[3]-Cal_St[3])/1.5
            s5 = (Real_St[4]-Cal_St[4])/1.5
            s6 = (Real_St[5]-Cal_St[5])/1.5
        new_var = torch.FloatTensor([s1*100, s2*100, s3*100, s4*100, s5*100, s6*100])
        pred_y = model(new_var)
        s1_data.append(s1)
        s2_data.append(s2)
        s3_data.append(s3)
        s4_data.append(s4)
        s5_data.append(s5)
        s6_data.append(s6)

        y1_pred.append(pred_y.detach().numpy()[0]*10)
        y2_pred.append(pred_y.detach().numpy()[1]*10)
        y3_pred.append(pred_y.detach().numpy()[2]*10)
        y4_pred.append(pred_y.detach().numpy()[3]*10)
        y5_pred.append(pred_y.detach().numpy()[4]*10)
        y6_pred.append(pred_y.detach().numpy()[5]*10)

        # ax.plot(x_data, y1_data, x_data, y2_data, x_data, y3_data, x_data, y4_data, x_data, y5_data, x_data, y6_data)
        # ax2.plot(x_data, s1_data, x_data, s2_data, x_data, s3_data, x_data, s4_data, x_data, s5_data, x_data, s6_data)
        # ax3.plot(x_data, y1_pred, x_data, y2_pred, x_data, y3_pred, x_data, y4_pred, x_data, y5_pred, x_data, y6_pred)
        # ax.plot(x_data, y1_pred, x_data, y1_data)
        # ax2.plot(x_data, y2_pred, x_data, y2_data)
        # ax3.plot(x_data, y3_pred, x_data, y3_data)
        ax4.plot(x_data, y4_pred, x_data, y4_data)
        ax5.plot(x_data, y5_pred, x_data, y5_data)
        ax6.plot(x_data, y6_pred, x_data, y6_data)
        # 그래프 축 설정 (예: 10초 이내 데이터만 표시)
        # ax.set_xlim(x - 10, x)
        # ax.set_ylim(-50, 50)
        #
        # ax2.set_xlim(x - 10, x)
        # ax2.set_ylim(-50, 50)
        #
        # ax3.set_xlim(x - 10, x)
        # ax3.set_ylim(-50, 50)

        ax4.set_xlim(x - 10, x)
        ax4.set_ylim(-50, 50)

        ax5.set_xlim(x - 10, x)
        ax5.set_ylim(-50, 50)

        ax6.set_xlim(x - 10, x)
        ax6.set_ylim(-50, 50)
        # 그래프 보여주기
        plt.show()
        plt.pause(0.001)

 
    if j == 30000:
        break
serverSocket.sendto(stop_command,atiAddress)

Sensor_data_trans = np.transpose(np.array([y1_data, y2_data, y3_data, y4_data, y5_data, y6_data]))
# Sensor_data_trans = np.delete(Sensor_data_trans, 0, 0)
Sensor_data_trans = np.append(Sensor_data_trans, np.zeros([Sensor_data_trans.shape[0],16]),1)
df = pd.DataFrame(np.append(Sensor_data_trans*[1, 1, 1, 50, 50, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], np.transpose(np.array([s1_data, s2_data, s3_data, s4_data, s5_data, s6_data])), 1))
df.to_csv('exp_data2.csv', index=False)
# df2 = pd.DataFrame(np.append(Sensor_data_trans*[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], np.transpose(np.array([y1_pred, y2_pred, y3_pred, y4_pred, y5_pred, y6_pred])), 1))
# df2.to_csv('error_calculate.csv', index=False)
print(Sensor_data)
