# ---------------------------------------------------.
# Shade 3Dの画像読み込み機能を利用して、.
# Substance Painterのテクスチャexportディレクトリをファイルダイアログで指定.
#
# @return エクスポートファイルのあるディレクトリ名,Project名 : TextureSet名  が返る.
# ---------------------------------------------------.
import string

# ファイルダイアログを表示して、ファイルパスを得る.
def get_image_path ():
    dirtyF = xshade.scene().dirty
    
    # 選択されている形状を一時保持.
    activeShapesList = xshade.scene().active_shapes
    
    # 画像を一時的に読み込み、ファイルパスだけ取得.
    xshade.scene().begin_creating()
    mImage = xshade.scene().create_master_image('test')
    name = ''
    try:
        mImage.load_image(None)
        name = mImage.image.path
    except:
        name = ''
    xshade.scene().end_creating()
    
    mImage.remove()     # 作業用に読み込んだマスターサーフェスは削除.

    # 選択をもとに戻す.
    xshade.scene().active_shapes = activeShapesList
    
    xshade.scene().dirty = dirtyF
    
    # パス名の「\」は「/」に置き換え.
    name = name.translate(string.maketrans('\\', '/'))    
    return name

# ディレクトリを取得し、その中のファイル一覧を取得.
result = ''
pathName = get_image_path()
if len(pathName) > 0:
    result = get_absPath_to_directory(pathName)    # フルパスからディレクトリだけ取り出し.

if result != None and result != "":
    fName = get_absPath_to_fileName(pathName)       # ファイル名を取り出し
    projectTexName = get_projectTextureName(fName)  # 「Project名 : TextureSet名」の取得.
    result += ',' + projectTexName

