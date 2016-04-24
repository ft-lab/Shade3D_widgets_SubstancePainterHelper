#-------------------------------------------------------.
# ファイル操作
#-------------------------------------------------------.
import struct
import urllib
import os
from os.path import join, relpath
from glob import glob

# ファイルのフルパスからディレクトリ名だけ返す.
def get_absPath_to_directory (absPath):
    return os.path.dirname(absPath)

# ファイルのフルパスからファイル名だけ返す.
def get_absPath_to_fileName (absPath):
    return os.path.basename(absPath)

# 指定のディレクトリ内にあるファイルを取得.
def get_files_name (searchPath):
    retFiles = []
    if os.path.isdir(searchPath) == False:
        return retFiles
    retFiles = [relpath(x, searchPath) for x in glob(join(searchPath, '*'))]
    return retFiles

# ファイル名からプロジェクト名とテクスチャセット名を取り出し.
# 「Project : TextureSet」を返す.
def get_projectTextureName (fileName):
    projectName    = ""
    textureSetName = ""
    
    # 拡張子のカット.
    ePos = fileName.rfind('.')
    if ePos <= 0: return ''
    fName = fileName[0:ePos]
    
    # Project名の取り出し.
    ePos1 = fName.find('_')
    if ePos1 <= 0: return ''
    projectName = fName[0:ePos1]
    
    # TextureSet名の取り出し.
    ePos2 = fName.rfind('_')
    if ePos2 <= 0: return ''
    textureSetName = fName[ePos1 + 1:ePos2]
    return projectName + ' : ' + textureSetName
    