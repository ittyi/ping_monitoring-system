# あるサブネット内のサーバが全て故障（ping応答がすべてN回以上連続でタイムアウト）している場合は、
# そのサブネット（のスイッチ）の故障とみなそう。
# 
# 各サブネット毎にネットワークの故障期間を出力できるようにする。
#
# 実行例：python network_failure_period.py N
# python network_failure_period.py 1
# python network_failure_period.py 5
# python network_failure_period.py 10
# python network_failure_period.py 11
#
# #
import sys
import datetime


# テスト時、ここtestx.txtのxを1～4に変更すると、用意したテストで実行できる
f = open('../test/test1.txt', 'r', encoding='UTF-8')
N = int(sys.argv[1])

# 例外処理 Nが行数より多い場合
if sum([1 for _ in f]) < N:
    print("Nがファイルの行数より大きいです。")
    sys.exit()
    
print("check")
count = 0
hyphen_count = 0
fault_condition = False
time_count_start = []
time_count_end = []
fail_server_address = []
Subnet_failure = []

# 本処理
datalist = f.readlines()
print("check", datalist)
for data in datalist:
    print("check")
    print(data)
    datasplit = data.split(",")
    index = len(datasplit)

    print(datasplit[index-1].replace( '\n' , '' ) == "-")
    if datasplit[index-1].replace( '\n' , '' ) == "-":
        hyphen_count += 1
        if hyphen_count >= N:
            print("check")
            Subnet_failure.append(
            datetime.datetime(
                year   = int(datasplit[0][0:4]),
                month  = int(datasplit[0][4:6]), 
                day    = int(datasplit[0][6:8]), 
                hour   = int(datasplit[0][8:10]),
                minute = int(datasplit[0][10:12]),
                second = int(datasplit[0][12:14])
                )
            )
            hyphen_count = 0


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
    elif (fault_condition == True) and datasplit[index-1].replace( '\n' , '' ) != "-":
        hyphen_count = 0
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


# 最後まで「-」で終わってしまった場合の処理 if
# 最後まで「-」が一つもなく正常 elif
# 「-」が一つ以上あり、応答が返ってきた場合
print ("N:", sys.argv[1]) 
if fault_condition == True:
    print("故障中のサーバIPv4アドレス:", fail_server_address[0])
    print("故障期間: 継続中")
elif time_count_start == [] or count < N:
    print("故障したサーバIPv4アドレス: なし")
    print("故障期間: なし")
else :
    for i in range(count):
        print("故障したサーバIPv4アドレス:", fail_server_address[i])
        print("故障期間:", time_count_end[i] - time_count_start[i])

print(time_count_start)
print(Subnet_failure)


f.close()