 # This file is a part of EC_serial_communication 
 # BSD 3-Clause License 
 # 
 # Copyright (c) 2019, Intelligent-distributed Cloud and Security Laboratory (ICNS Lab.) 
 # All rights reserved. 
 # 
 # Redistribution and use in source and binary forms, with or without 
 # modification, are permitted provided that the following conditions are met: 
 # 
 # 1. Redistributions of source code must retain the above copyright notice, this 
 #    list of conditions and the following disclaimer. 
 # 
 # 2. Redistributions in binary form must reproduce the above copyright notice, 
 #    this list of conditions and the following disclaimer in the documentation 
 #    and/or other materials provided with the distribution. 
 # 
 # 3. Neither the name of the copyright holder nor the names of its 
 #    contributors may be used to endorse or promote products derived from 
 #    this software without specific prior written permission. 
 # 
 # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
 # AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
 # IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
 # DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
 # FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
 # DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
 # SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
 # CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
 # OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
 # OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 
 
 
 # title           : serial_Monitoring.py 
 # description     : Python, SA(Stand Alone) Data monitoring through serial communication 
 # author          : Jihoo Chun 
 # date            : 20190822 
 # version         : 0.3 
 # notes           : This EC_serial_communication is an implementation of edge cloud for communicating 
 # 				 self-driving cart and edge cloud. 


import serial
import numpy as np
import matplotlib.pyplot as plt
# % matplotlib
# notebook

ser = serial.Serial('COM4', 9600, timeout=0)

Lsonar = 0
Rsonar = 0
Lencoder = 0
Rencoder = 0

sensor = []

fig = plt.figure()  # 그래프 창 생성, (9,9)형식으로 가로세로 9인치 설정가능
########sonar##### 나중에 메인문에 ax_sonar하나더해서 label붙여서 좌우 구분
ax_sonar = fig.add_subplot(211)  # ax라는 그림표하나 생성 추후 각 센서별로 여러개 만들예정, 11은 1행 1열에 위치
########Encoder#####
# ax_Encoder=fig.add_subplot(212)

# plt.ion()

####initialize###
# ax.set_title('Sensor plot')
ax_sonar.set_xlabel('PSD')
ax_sonar.set_ylabel('distance_cm')
ax_sonar.set_ylim([0, 200])  # 최대치 설정
ax_sonar.legend()

# #엔코더쓰려면 새로 좌표 정해서 쓰기
# ax_Encoder.set_xlabel('Encoder')
# ax_Encoder.set_ylabel('value')
# ax_Encoder.legend()

x = 0
fig.show()


def draw_all_plot(x):
    ax_sonar.plot(x, int(PSD), 'or', label='left')
    # ax_sonar.plot(x,int(Rsonar),'ob',label='right')


# ax_Encoder.plot(x,int(Lencoder),'or',label='left')
# ax_Encoder.plot(x,int(Rencoder),'ob',label='right')

def switch1(x):
    global PSD  # Lsonar
    global Rsonar
    global Lencoder
    global Rencoder

    if x == "LS":
        PSD = tmp
    elif x == 'RS':
        Rsonar = tmp
    elif x == 'LE':
        Lencoder = tmp
    elif x == 'RE':
        Rencoder = tmp


def parsing_data(data):
    global tmp
    #     global value

    data.pop()  # tail 제거
    a = data[0]  # head 첫번째값
    b = data[1]  # head 두번째값
    c = a + b  # 총 head 'LS' 이런식으로 결과값 나옴
    del data[0:2]  # 센서값만 추출하기 위해 head 제거
    tmp = ''.join(data)  ##최종 센서값
    switch1(c)  # parsing


#   return tmp


# print(Lsonar)

while 1:
    for c in ser.read():
        sensor.append(chr(c))
        #  plt.clf() #그래프초기화
        if c == 84:  # T의 아스키 코드값, tail이 올때까지 데이터를 합친다
            parsing_data(sensor)
            del sensor[:]  # line 초기화
            draw_all_plot(x)
            x += 1
            ax_sonar.figure.canvas.draw()
            # ax_Encoder.figure.canvas.draw()
            plt.pause(0.1)

# 연습
#     counter += 1
#     del sensor[:] #line 초기화
#     ax.plot(x,counter,'or') #x축,y축값, 그래프종류
#     x+=1
#     ax.figure.canvas.draw()
#     plt.pause(0.1)
