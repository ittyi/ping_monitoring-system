# 故障状態のサーバアドレスとそのサーバの故障期間を出力するプログラムを作成
# 
# pingがタイムアウトした場合を故障とみなし、最初にタイムアウトしたときから、
# 次にpingの応答が返るまでを故障期間とする。
#
# 実行：python server_failure_detection.py
# お手数ですが、プログラム内14行目のファイルへのパスをいじってテストしてください。
# 
# 改善点：datetimeの関数化
# #
import datetime

LOG_FILE_NAME = '../test/test4.txt'

# テスト時、ここtestx.txtのxを1～4に変更すると、用意したテストで実行できる
f = open(LOG_FILE_NAME, 'r', encoding='UTF-8')

count = 0
fault_condition = False
time_count_start = []
time_count_end = []
fail_server_address = []

# 本処理
datalist = f.readlines()
for data in datalist:
    datasplit = data.split(",")
    index = len(datasplit)

    if datasplit[index-1].replace( '\n' , '' ) == "-":
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
if fault_condition == True:
    print("故障中のサーバIPv4アドレス:", fail_server_address[0])
    print("故障期間: 継続中")
elif time_count_start == []:
    print("故障したサーバIPv4アドレス: なし")
    print("故障期間: なし")
else :
    for i in range(count):
        print("故障したサーバIPv4アドレス:", fail_server_address[i])
        print("故障期間:", time_count_end[i] - time_count_start[i])


f.close()
