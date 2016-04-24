# -------------------------------------------------------.
# Substance Painterエクスポートのテクスチャリストの管理.
#  	$project_$textureSet_Diffuse
#	$project_$textureSet_Normal
#	$project_$textureSet_Roughness
#	$project_$textureSet_Specular
#   の4枚から構成される.
# 画像を読み込んだときのフォルダを保持し、
# その中のリストを保持.
#
# @param[in]  f_location      カレントパス (string).
# @param[in]  f_filePath      exportテクスチャのあるパス (string).
# -------------------------------------------------------.
import urllib
import os
import os.path

# 保存するファイル名.
DATA_FILE_NAME = 'texturesList_data.txt'

filePath = urllib.unquote(f_location) + '/datas'
if os.path.isdir(filePath) == False:
    os.mkdir(filePath)

# ファイルを開く.
saveFile = filePath + '/' + DATA_FILE_NAME
f = open(saveFile, 'w')
if f != None:
    wStr = 'exportFilePath=' + str(urllib.unquote(f_filePath)) + '\n'
    f.writelines(wStr)

    # ファイルを閉じる.
    f.close()

result = ''
