# ---------------------------------------------.
# Shade 3Dの言語別のテキストメッセージを取得.
# text_ja.txt / text_en.txt からキーに対するテキストを取得.
# @param[in]  f_location      カレントパス (string).
# @param[in]  f_key           キー値.
# @param[in]  f_lang          言語。jaの場合は日本語.
# @return キーに対応する値を返す.
# ---------------------------------------------.
import urllib
import os
import os.path

targetkey = urllib.unquote(f_key)

# ファイル名.
resFileName = 'text_en.txt'
if urllib.unquote(f_lang) == 'ja':
    resFileName = 'text_ja.txt'
   
targetFile = urllib.unquote(f_location) + '/' + resFileName

result = ''
if os.path.exists(targetFile) == True:
    f = open(targetFile, 'r')     # ファイルを開く.
    if f != None:
        lineStr = f.readline()
        while lineStr:
            lineStr = lineStr.strip()		# 行頭、行末の改行や空白を削除.
            if len(lineStr) > 0 and lineStr[0] != '#':
                ePos = lineStr.find('=')
                if ePos > 0:
                    keyStr = lineStr[0:ePos].strip()
                    valStr = lineStr[ePos + 1:].strip()
                    if keyStr == targetkey:
                        result = valStr
            lineStr = f.readline()
        f.close()       # ファイルを閉じる.

# 文字列の前後のダブルクォーテーションを省く.
if len(result) > 0:
   stPos = result.find('"')
   if stPos == 0:
        endPos = result.find('"', stPos + 1)
        if endPos > 0:
            result = result[stPos + 1:endPos]
            