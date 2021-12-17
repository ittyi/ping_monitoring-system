# まず、ログファイルを”読み込める”ようにする。
# ファイルをパラメータとして。。という文言はないため、何とかして別フォルダにいるファイルを読み込む必要がある。

f = open('../test/test1.txt', 'r', encoding='UTF-8')
print(f)

data = f.read()

print(data)

f.close()