# 直近m回の平均応答時間がtミリ秒を超えた場合は、
# サーバが過負荷状態になっているとみなそう。
# 各サーバの過負荷状態となっている期間を出力できるように。
# 
# mとtはプログラムのパラメータとして与えられるようにする。
#
# 実行例：python overload_check.py m t
# python overload_check.py 2 3
# python overload_check.py 2 500
# python overload_check.py 3 3
# python overload_check.py 5 3
# python overload_check.py 11 3
# 
# #
import sys
import datetime

m = int(sys.argv[1])
t = int(sys.argv[2])
print ("m:", sys.argv[1]) 
print ("t:", sys.argv[2]) 

# テスト時、ここtestx.txtのxを1～4に変更すると、用意したテストで実行できる
f = open('../test/test4.txt', 'r', encoding='UTF-8')

# 例外処理 mが行数より多い場合
if sum([1 for _ in f]) < m:
    print("mがping実行回数より大きいです。")
    sys.exit()

count = 0
failure_count = 0
fault_condition = False
time_count_start = []
time_count_end = []
fail_server_address = []
overload_checksum = 0
overload_pick_start = []
overload_pick_end = []

# 本処理
datalist = f.readlines()
for data in datalist:
    datasplit = data.split(",")
    index = len(datasplit)

    # サーバ過負荷状態判定
    count += 1
    if count == 1 and datasplit[index-1].replace( '\n' , '' ) != "-":
        overload_pick_start.append(datasplit[0])
        overload_checksum += int(datasplit[index-1].replace( '\n' , '' ))
    elif count == 1 and datasplit[index-1].replace( '\n' , '' ) == "-":
        overload_pick_start.append(datasplit[0])
    elif count < m and datasplit[index-1].replace( '\n' , '' ) != "-":
        overload_checksum += int(datasplit[index-1].replace( '\n' , '' ))
    elif count >= m and datasplit[index-1].replace( '\n' , '' ) == "-":
        overload_checksum /= m
        if overload_checksum > t:
            overload_pick_end.append(datasplit[0])
        else :
            overload_pick_start.pop()
        count = 0
        overload_checksum = 0
    elif count >= m:
        overload_checksum += int(datasplit[index-1].replace( '\n' , '' ))
        overload_checksum /= m
        if overload_checksum > t:
            overload_pick_end.append(datasplit[0])
        else :
            overload_pick_start.pop()
        count = 0
        overload_checksum = 0
    

    # サーバの故障期間
    if datasplit[index-1].replace( '\n' , '' ) == "-":
        failure_count += 1
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
# print ("N:", sys.argv[1]) 
# print ("N:", sys.argv[2]) 
if fault_condition == True:
    print("故障中のサーバIPv4アドレス:", fail_server_address[0])
    print("故障期間: 継続中")
elif time_count_start == [] or failure_count < m:
    print("故障したサーバIPv4アドレス: なし")
    print("故障期間: なし")
else :
    for i in range(failure_count):
        print("故障したサーバIPv4アドレス:", fail_server_address[i])
        print("故障期間:", time_count_end[i] - time_count_start[i])


# サーバ過負荷状態出力
if overload_pick_end == []:
    print("サーバ過負荷状態なし")
else :
    index_start = len(overload_pick_start)
    index_end = len(overload_pick_end)
    print(index_start)
    print(index_end)
    for i in range(len(overload_pick_start)):
        print("サーバ過負荷状態 "+ str(i+1) + "回目")
        print("開始", overload_pick_start[i])
        if index_end <= 0:
            print("監視ログ終了")
        else :
            print("終了", overload_pick_end[i])
        
        index_end -= 1


f.close()