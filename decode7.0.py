import csv
import os
import math
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

#[1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1,
#  0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1]
OSCSMAPLING_RATE = 1.25 #GHz   12point
INTERNAL_FREQUENCY = 100
max_shift = 200-128   ##AWG取的碼數-打的碼數
ANS = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ANS_file_path = r"C:\Users\ASUS\Desktop\python\Q-bit\signal_data\Mcodeset128.txt"
 # 请替换为你的文件名
with open(ANS_file_path, "r") as file:
    # 读取文件内容并存储为列表
    ANS = [int(line.strip()) for line in file.readlines()]

# 关闭文件
file.close()
signal_width = 1+math.floor(12*OSCSMAPLING_RATE/12.5)

# 用於存儲第E列數據的列表
data1 = []
data0 = []
# 建立一個隱藏的Tkinter窗口，不會實際顯示出來
root = tk.Tk()
root.withdraw()

# 讓檔案選擇對話框顯示在最前面
root.attributes("-topmost", True)


# 彈出檔案選擇對話框並取得使用者選擇的檔案路徑1
#file_path1 = filedialog.askopenfilename(title="SPAD1.txt", filetypes=[("Text Files", "*.csv")])
file_path1 = r"C:\Users\ASUS\Desktop\python\Q-bit\signal_data\spad090_Ch1.csv"
with open(file_path1, 'r', newline='') as csvfile:
    # 使用csv.reader來讀取CSV檔案
    csv_reader = csv.reader(csvfile)
    
    # 迭代每一行
    for row in csv_reader:
        # 確保行中有足夠的列數
        if len(row) > 4:
            # 添加第E列數據到e_column_data列表中
            data1.append(row[4])

# 彈出檔案選擇對話框並取得使用者選擇的檔案路徑0
#file_path2 = filedialog.askopenfilename(title="SPAD2.txt", filetypes=[("Text Files", "*.csv")])
file_path0 = r"C:\Users\ASUS\Desktop\python\Q-bit\signal_data\spad090_Ch3.csv"
# 讀取文件並處理資料2
with open(file_path0, 'r', newline='') as csvfile:
    # 使用csv.reader來讀取CSV檔案
    csv_reader = csv.reader(csvfile)
    
    # 迭代每一行
    for row in csv_reader:
        # 確保行中有足夠的列數
        if len(row) > 4:
            # 添加第E列數據到e_column_data列表中
            data0.append(row[4])

numbers1 = [float(value) for value in data1]
numbers2 = [float(value) for value in data0]
abs_number1 = [abs(x) for x in numbers1]
abs_number2 = [abs(x) for x in numbers2]
M_numbers1 = max(abs_number1)
M_numbers2 = max(abs_number2)
V = 0.7
numbers1 = [0 if abs(num)< V*M_numbers1 else num for num in numbers1]
numbers1 = [1 if abs(num)>= V*M_numbers1 else num for num in numbers1]
numbers2 = [0 if abs(num)< V*M_numbers2 else num for num in numbers2]
numbers2 = [1 if abs(num)>= V*M_numbers2 else num for num in numbers2]

'''
with open('C:\\Users\\USER\\Desktop\\Q-bit\\numbers1.txt', 'w') as file:
    for num in sorted(numbers1):
        file.write(str(num) + '\n')
with open('C:\\Users\\USER\\Desktop\\Q-bit\\numbers2.txt', 'w') as file:
    for num in sorted(numbers2):
        file.write(str(num) + '\n')
'''
Num_1 = []
for index, value in enumerate(numbers1, start=1):
    Num_1.append([value, index])
with open(r'C:\Users\ASUS\Desktop\python\Q-bit\rudata\\Num_1.txt', 'w') as file:
    for num in Num_1:
        file.write(str(num) + '\n')
Num_0 = []
for index, value in enumerate(numbers2, start=1):
    Num_0.append([value, index])
with open(r'C:\Users\ASUS\Desktop\python\Q-bit\rudata\\Num_2.txt', 'w') as file:
    for num in Num_0:
        file.write(str(num) + '\n')
##去單一雜訊
result_data1 = []
result_data0 = []
##去底躁
i = 0 
while i < len(Num_1):
    if Num_1[i][0] == 1:
        signal = [Num_1[i]]
        i += 1

        while i < len(Num_1) and Num_1[i][0] == 1:
            signal.append(Num_1[i])
            i += 1

        if len(signal) < signal_width:
            for j in range(len(signal)):
                result_data1.append([0, signal[j][1]])
        else:
            result_data1.extend(signal)
    else:
        result_data1.append(Num_1[i])
        i += 1
i = 0
while i < len(Num_0):
    if Num_0[i][0] == 1:
        signal = [Num_0[i]]
        i += 1

        while i < len(Num_0) and Num_0[i][0] == 1:
            signal.append(Num_0[i])
            i += 1

        if len(signal) < signal_width:
            for j in range(len(signal)):
                result_data0.append([0, signal[j][1]])
        else:
            result_data0.extend(signal)
    else:
        result_data0.append(Num_0[i])
        i += 1

##選擇1
with open(r'C:\Users\ASUS\Desktop\python\Q-bit\rudata\\result_data1.txt', 'w') as file:
    for num in result_data1:
        file.write(str(num) + '\n')
with open(r'C:\Users\ASUS\Desktop\python\Q-bit\rudata\\result_data0.txt', 'w') as file:
    for num in result_data0:
        file.write(str(num) + '\n')
Num_1_select1 = [row for row in result_data1 if row[0] != 0]
Num_0_select1 = [row for row in result_data0 if row[0] != 0]
with open(r'C:\Users\ASUS\Desktop\python\Q-bit\rudata\\Num_1_select1test.txt', 'w') as file:
    for num in Num_1_select1:
        file.write(str(num) + '\n')
with open(r'C:\Users\ASUS\Desktop\python\Q-bit\rudata\\Num_0_select1test.txt', 'w') as file:
    for num in Num_0_select1:
        file.write(str(num) + '\n')

if not Num_1_select1:
    print("Num_1_select1 序列為空，程式停止運作。")
    exit()  # 停止程式運行
elif not Num_0_select1:
    print("Num_0_select1 序列為空，程式停止運作。")
    exit()  # 停止程式運行
else:
    pass
##去相鄰同數據
def process_data(data):
    filtered_data = []

    #處理第一筆記錄
    current_block = [data[0]]
    
    for i in range(1, len(data)):
        prev_record = data[i - 1]
        current_record = data[i]
        
        if current_record[1] == prev_record[1] + 1:
            # 若相鄰，只有兩項相鄰時保留前一項
            if len(current_block) == 2:
                filtered_data.append(current_block[0])
            current_block = [prev_record]
        else:
            # 如果不相鄰，處理目前區塊並將其新增至結果中
            filtered_data.extend(current_block)
            current_block = [current_record]

    #處理最後一個區塊
    filtered_data.extend(current_block)

    return filtered_data

with open(r'C:\Users\ASUS\Desktop\python\Q-bit\rudata\\Num_1_select1.txt', 'w') as file:
    for num in Num_1_select1:
        file.write(str(num) + '\n')
with open(r'C:\Users\ASUS\Desktop\python\Q-bit\rudata\\Num_0_select1.txt', 'w') as file:
    for num in Num_0_select1:
        file.write(str(num) + '\n')
Num_11_select1 = process_data(Num_1_select1)
Num_01_select1 = process_data(Num_0_select1)

with open(r'C:\Users\ASUS\Desktop\python\Q-bit\rudata\Num_11_select1.txt', 'w') as file:
    for num in Num_11_select1:
        file.write(str(num) + '\n')
with open(r'C:\Users\ASUS\Desktop\python\Q-bit\rudata\Num_01_select1.txt', 'w') as file:
    for num in Num_01_select1:
        file.write(str(num) + '\n')

##計算間距
for i in range(len(Num_11_select1) - 1):
    interval = Num_11_select1[i + 1][1] - Num_11_select1[i][1]
    Num_11_select1[i].append(interval)
Num_11_select1.pop()
for i in range(len(Num_01_select1) - 1):
    interval = Num_01_select1[i + 1][1] - Num_01_select1[i][1]
    Num_01_select1[i].append(interval)
Num_01_select1.pop()
#列印帶有第三列的數據
with open(r'C:\Users\ASUS\Desktop\python\Q-bit\rudata\\Num_11_select3.txt', 'w') as file:
    for num in Num_11_select1:
        file.write(str(num) + '\n')
with open(r'C:\Users\ASUS\Desktop\python\Q-bit\rudata\\Num_01_select3.txt', 'w') as file:
    for num in Num_01_select1:
        file.write(str(num) + '\n')
third_column1 = [row[2] for row in Num_11_select1]
max_value1 = max(third_column1)
min_value1 = min(third_column1)
third_column0 = [row[2] for row in Num_01_select1]
max_value0 = max(third_column0)
min_value0 = min(third_column0)
#average_value = round(sum(third_column) / len(third_column))
print("間距最大值1:", max_value1)
print("間距最小值1:", min_value1)
print("間距最大值0:", max_value0)
print("間距最小值0:", min_value0)
#print("平均值:", average_value)

with open(r'C:\Users\ASUS\Desktop\python\Q-bit\rudata\\Num_11_select1column3.txt', 'w') as file:
    for num in third_column1:
        file.write(str(num) + '\n')
with open(r'C:\Users\ASUS\Desktop\python\Q-bit\rudata\\Num_21_select1column3.txt', 'w') as file:
    for num in third_column0:
        file.write(str(num) + '\n')

Num_01_select1 = [[2,item[1],item[2]] if item[0]==1 else item for item in Num_01_select1]

final_code = Num_01_select1 + Num_11_select1

final_code = sorted(final_code, key=lambda x: x[1])
with open(r'C:\Users\ASUS\Desktop\python\Q-bit\rudata\\finaloriginal_code.txt', 'w') as file:
    for num in final_code:
        file.write(str(num) + '\n')

final_code = [item[0] for item in final_code]
final_code = [0 if i == 2 else i for i in final_code]
with open(r'C:\Users\ASUS\Desktop\python\Q-bit\rudata\\final_code.txt', 'w') as file:
    for num in final_code:
        file.write(str(num) + '\n')
final_code = final_code[::-1]
max_shift = abs(len(ANS)-len(final_code))
if len(final_code) == len(ANS):
    print("訊號長度一致")
    ###序列對準
    #max_shift = 5
    best_shift = 0
    best_correlation = 0

    # 尝试不同的位移值，以找到最佳的相关性
    for shift in range(-max_shift, max_shift + 1):
        correlation = np.correlate(ANS, np.roll(final_code, shift), mode='valid')
        if correlation > best_correlation:
            best_correlation = correlation
            best_shift = shift

    # 使用找到的最佳位移值来还原list2
    final_code = final_code[-best_shift:] + final_code[:-best_shift]
    ###
    xor = [a^b for a,b in zip(final_code,ANS)]
    count = xor.count(1)
elif len(final_code) > len(ANS):
    print(abs(len(ANS)-len(final_code)),f'idealy{200-128}')
    final_code = final_code[:(len(ANS)-len(final_code))]
    print("訊號長度大於ANS刪去末端訊號(QBER error)")
    ###序列對準
    #max_shift = 5
    best_shift = 0
    best_correlation = 0

    # 尝试不同的位移值，以找到最佳的相关性
    for shift in range(-max_shift, max_shift + 1):
        correlation = np.correlate(ANS, np.roll(final_code, shift), mode='valid')
        if correlation > best_correlation:
            best_correlation = correlation
            best_shift = shift

    # 使用找到的最佳位移值来还原list2
    final_code = final_code[-best_shift:] + final_code[:-best_shift]
    ###
    xor = [a^b for a,b in zip(final_code,ANS)]
    count = xor.count(1)
elif len(final_code) < len(ANS):
    final_code += [0]*(len(ANS)-len(final_code))
    print("訊號長度小於ANS後方補0(QBER error)")
    ###序列對準
    #max_shift = 5
    best_shift = 0
    best_correlation = 0

    # 尝试不同的位移值，以找到最佳的相关性
    for shift in range(-max_shift, max_shift + 1):
        correlation = np.correlate(ANS, np.roll(final_code, shift), mode='valid')
        if correlation > best_correlation:
            best_correlation = correlation
            best_shift = shift

    # 使用找到的最佳位移值来还原list2
    final_code = final_code[-best_shift:] + final_code[:-best_shift]
    ###
    xor = [a^b for a,b in zip(final_code,ANS)]
    count = xor.count(1)
print(best_shift)
QBER = round(100*count/(len(final_code)),3)
print(f'QBER = {QBER}%')

with open(r'C:\Users\ASUS\Desktop\python\Q-bit\rudata\\final_code_shift.txt', 'w') as file:
    for num in final_code:
        file.write(str(num) + '\n')
