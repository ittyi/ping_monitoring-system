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


f = open('../test/test1.txt', 'r', encoding='UTF-8')
# print(f)

count = 1
fault_condition = False
time_count_start = 0
time_count_end = 0
fail_server_address = ""

datalist = f.readlines()
for data in datalist:
    print(data)
    # print(count)
    count += 1

    datasplit = data.split(",")
    print(datasplit)
    index = len(datasplit)
    print(datasplit[index-1])

    if datasplit[index-1] == ("-\n" or "-"):
        fault_condition = True
        time_count_start = datetime.datetime(
            year=int(datasplit[0][0:4]),
            month=int(datasplit[0][4:6]), 
            day=int(datasplit[0][6:8]), 
            hour=int(datasplit[0][8:10]),
            minute=int(datasplit[0][10:12]),
            second=int(datasplit[0][12:14])
            )
        fail_server_address = datasplit[1]
    
    if (fault_condition == True) and datasplit[index-1] != ("-\n" or "-"):
        print("check")
        fault_condition = True
        time_count_end = datetime.datetime(
            year=int(datasplit[0][0:4]),
            month=int(datasplit[0][4:6]), 
            day=int(datasplit[0][6:8]), 
            hour=int(datasplit[0][8:10]),
            minute=int(datasplit[0][10:12]),
            second=int(datasplit[0][12:14])
            )
 


print(fault_condition)
print("故障したサーバIPv4アドレス:", fail_server_address)
print(time_count_start)
print(time_count_end)
print("故障期間:", time_count_end - time_count_start)

f.close()