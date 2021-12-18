# 故障状態のサーバアドレスとそのサーバの故障期間を出力するプログラムを作成
# 
# まず、ログファイルを”読み込める”ようにする。
# ファイルをパラメータとして。。という文言はないため、何とかして別フォルダにいるファイルを読み込む必要がある。
# 
# pingがタイムアウトした場合を故障とみなし、最初にタイムアウトしたときから、
# 次にpingの応答が返るまでを故障期間とする。
#
# 
# #
import datetime


f = open('../test/test2.txt', 'r', encoding='UTF-8')
# print(f)

count = 0
fault_condition = False
time_count_start = []
time_count_end = []
fail_server_address = []

datalist = f.readlines()
for data in datalist:
    print(data)
    # print(count)

    datasplit = data.split(",")
    print(datasplit)
    index = len(datasplit)
    print(datasplit[index-1])

    if datasplit[index-1] == ("-\n" or "-"):
        print("check")
        count += 1
        fault_condition = True
        time_count_start.append(
            datetime.datetime(
                year   = int(datasplit[0][0:4]),
                month  = int(datasplit[0][4:6]), 
                day    = int(datasplit[0][6:8]), 
                hour   = int(datasplit[0][8:10]),
                minute = int(datasplit[0][10:12]),
                second = int(datasplit[0][12:14])
                )
        )
        fail_server_address.append(datasplit[1])
    
    if (fault_condition == True) and datasplit[index-1] != ("-\n" or "-"):
        print("check2")
        fault_condition = False
        time_count_end.append(
            datetime.datetime(
                year   = int(datasplit[0][0:4]),
                month  = int(datasplit[0][4:6]), 
                day    = int(datasplit[0][6:8]), 
                hour   = int(datasplit[0][8:10]),
                minute = int(datasplit[0][10:12]),
                second = int(datasplit[0][12:14])
                )
        )

print("count:", count, len(time_count_start))
print(fault_condition)
print(time_count_start)
print(time_count_end)


# 最後まで「-」で終わってしまった場合の処理 if
# 最後まで「-」が一つもなかった elif
# 正常 else
if fault_condition == True:
    print("故障中のサーバIPv4アドレス:", fail_server_address[0])
    print("故障期間: 継続中")
elif time_count_start == []:
    print("故障したサーバIPv4アドレス: なし")
    print("故障期間: なし")
elif len(time_count_start) == 1:
    print("check3")
    print("故障したサーバIPv4アドレス:", fail_server_address[0])
    print("故障期間:", time_count_end[0] - time_count_start[0])
else :
    for i in range(count):
        print("故障したサーバIPv4アドレス:", fail_server_address[i])
        print("故障期間:", time_count_end[i] - time_count_start[i])


f.close()
