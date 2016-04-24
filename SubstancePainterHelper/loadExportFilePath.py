# -------------------------------------------------------.
# Substance Painterエクスポートのファイルパスを取得.
# @param[in]  f_location      カレントパス (string).
# -------------------------------------------------------.
import struct
import urllib
import os
import os.path

# 保存するファイル名.
DATA_FILE_NAME = 'texturesList_data.txt'

targetFile = urllib.unquote(f_location) + '/datas/' + DATA_FILE_NAME

result = ''
if os.path.exists(targetFile) == True:
    f = open(targetFile, 'r')     # ファイルを開く.
    if f != None:
        lineStr = f.readline()
        while lineStr:
            lineStr = lineStr.strip()		# 行頭、行末の改行や空白を削除.
            if len(lineStr) != 0:
                fPos = lineStr.find('exportFilePath')
                if fPos >= 0:
                    ePos = lineStr.find('=', fPos + 1)
                    if ePos > 0:
                        result = lineStr[(ePos + 1):]
                        result = result.strip()
                        break
            lineStr = f.readline()
        f.close()       # ファイルを閉じる.
