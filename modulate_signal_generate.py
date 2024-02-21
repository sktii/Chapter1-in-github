### Author = Yen ###

import numpy as np
import matplotlib.pyplot as plt
import os

##檔案儲存位置
output_directory = r'C:\Users\ASUS\Desktop'  

input_text = input("請輸入要轉換成ASCII的文字: ")
# 將文字轉換為ASCII 2進制列表
ascii_binary_list = []
ascii_binary_listseperate = []

for char in input_text:
    # 將字符轉換為ASCII值
    ascii_value = ord(char)
    # 將ASCII值轉換為二進制字符串 
    binary_representation = bin(ascii_value)[2:]
    # 將二進制字符串添加到列表中
    ascii_binary_list.append(binary_representation)
    binary_list1 = [int(bit) for bit in binary_representation]
    
    # 將整數列表添加到ASCII 2進制列表中
    ascii_binary_listseperate.extend(binary_list1)
# 打印結果
print("ASCII 2進制列表:", ascii_binary_list)
print("ASCII 2進制列表tseperate:", ascii_binary_listseperate)

#### 
count = 0
Mcodeset = ascii_binary_listseperate  #ASCII 編碼
#Mcodeset = [1,1,0,0,1,1] # <=1
Scodeset = np.ones(len(Mcodeset)) #固定脈衝(也可任意編碼)
#Scodeset = [1, 1, 1, 1, 1]
delaytime = 1.5  # GHZ
Sampling_rate = 120  # GHZ 根據儀器調整
M_dutycycle = 0.4
S_dutycycle = 0.5  
Mastermodify = 0.00
####

signal_length = round(Sampling_rate / delaytime)       
S_phase =   360-(M_dutycycle*360/2+180-S_dutycycle*360/2)       #0~360 預設為在Master訊號的中間
M_phase = 0   # 不改Master phase     
print('S_phase',S_phase)
M_V = 1  
S_V = 1
zero_sequence = np.zeros(signal_length)
MSIGNAL = np.copy(zero_sequence)
SSIGNAL = np.copy(zero_sequence)
phaseshift = np.copy(zero_sequence)
#Mphase_shift_length = round(M_phase * signal_length / 360)
#print("Mshiftlength",Mphase_shift_length)
#Mphase_shift = np.zeros(Mphase_shift_length)
Sphase_shift_length = round(S_phase * signal_length / 360)
Sphase_shift = np.zeros(round(S_phase * signal_length / 360))
print("Sshiftlength",Sphase_shift_length)
M_signal_length = int(M_dutycycle * signal_length)
S_signal_length = int(S_dutycycle * signal_length)
M_signal = np.full(M_signal_length, M_V)
S_signal = np.full(S_signal_length, S_V)
insert_position = 0
MSIGNAL[insert_position:insert_position + M_signal_length] = M_signal
SSIGNAL[insert_position:insert_position + S_signal_length] = S_signal


#波型合成
def combine_waves(wave_weights, sub_wave):
    combined_wave = []

    for weight in wave_weights:
        weighted_sub_wave = [value * weight for value in sub_wave]
        combined_wave.extend(weighted_sub_wave)

    return np.array(combined_wave)  # 將結果轉換為numpy數組

print('phaseshift',len(phaseshift))
Master_signal = combine_waves(Mcodeset,MSIGNAL)
Slave_signal = combine_waves(Scodeset,SSIGNAL)
#Master_signal = np.insert(phaseshift, Mphase_shift_length, Master_signal)
slave_shift = Slave_signal[0:Sphase_shift_length]
Slave_signal = np.delete(Slave_signal, slice(0, Sphase_shift_length)) 
Slave_signal = np.insert(Slave_signal,len(Slave_signal),slave_shift)

# 取得數組的長度
length = len(Master_signal)
count = 0
# 遍歷陣列並執行操作
for i in range(length):
    if Master_signal[i] == 1:
        count += 1
        Master_signal[i] += count*Mastermodify


#Slave_signal = np.insert(phaseshift, Sphase_shift_length, Slave_signal)
# 保存數據到txt檔，每個元素佔據一列

# 保存 Master_signal 到文件
master_file_path = os.path.join(output_directory, 'Master_signal.txt')
np.savetxt(master_file_path, Master_signal.reshape(-1, 1), fmt='%.2f', delimiter=',')

# 保存 Slave_signal 到文件
slave_file_path = os.path.join(output_directory, 'Slave_signal.txt')
np.savetxt(slave_file_path, Slave_signal.reshape(-1, 1), fmt='%.2f', delimiter=',')

# 創建一個視窗，包含三個子圖，一列一行
fig, axes = plt.subplots(3, 1, figsize=(6, 12))
# 繪製Slave訊號
x_values_slave = range(len(Slave_signal))
axes[0].plot(x_values_slave, Slave_signal, label='Slave Signal Data', linewidth=0.5, linestyle='-')
axes[0].set_xlabel('time')
axes[0].set_ylabel('V')
axes[0].set_title('Slave')
axes[0].set_xlim(0, len(Slave_signal))
# 繪製Master信號
x_values_master = range(len(Master_signal))
axes[1].plot(x_values_master, Master_signal, label='Master Signal Data', linewidth=0.5, linestyle='-')
axes[1].set_xlabel('time')
axes[1].set_ylabel('V')
axes[1].set_title('Master')
axes[1].set_xlim(0, len(Slave_signal))
# 調整兩個信號的長度以匹配較長的信號
if len(Slave_signal) < len(Master_signal):
    Slave_signal = np.pad(Slave_signal, (0, len(Master_signal) - len(Slave_signal)), 'constant')
elif len(Master_signal) < len(Slave_signal):
    Master_signal = np.pad(Master_signal, (0, len(Slave_signal) - len(Master_signal)), 'constant')
# 在第三張圖上繪製兩個訊號
x_values = range(max(len(Slave_signal), len(Master_signal)))
axes[2].plot(x_values, Slave_signal, label='Slave Signal Data', linewidth=1, linestyle='-', color='b')
axes[2].plot(x_values, Master_signal, label='Master Signal Data', linewidth=1, linestyle='-', color='r')
axes[2].set_xlabel('time')
axes[2].set_ylabel('V')
axes[2].set_title('Combined Plot')
axes[2].set_xlim(0, len(Slave_signal))
# 調整子圖之間的間距
plt.tight_layout()
plt.show()
fig.savefig(os.path.join(output_directory, 'my_plot.png'))
