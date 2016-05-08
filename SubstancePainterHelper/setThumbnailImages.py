# -------------------------------------------------------.
# 4枚のテクスチャサムネイル画像を出力.
# @param[in]  f_location       カレントパス (string).
# @param[in]  f_filePath        exportテクスチャのあるパス (string).
# @param[in]  f_projectTexName 「project : textureSet」の値(string).
# @return diffuse,normal,roughness,specular のサムネイル画像名が返る.
# -------------------------------------------------------.
import urllib
import os
import os.path

# 保存するファイルパス.
TEX_FILE_PATH  = urllib.unquote(f_location) + '/datas'

# Exportファイルのあるパス.
EXPORT_FILE_PATH = urllib.unquote(f_filePath)

# サムネイルサイズ.
THUMBNAIL_WIDTH = 80
THUMBNAIL_HEIGHT = 80

# 保存するファイル名.
texNameList = ['diffuse_thumb.png', 'normal_thumb.png', 'roughness_thumb.png', 'specular_thumb.png']

# ディレクトリ中のファイル一覧を取得.
dirPath = urllib.unquote(f_filePath)
rFilesList = get_files_name(dirPath)

# ----------------------------------------------------.
# 画像が存在するかチェックし、ファイル名を取得.
# ----------------------------------------------------.
def checkImagesFile (projectName, textureSetName, texType = 0):
    fileBaseName =  projectName + '_' + textureSetName
    
    if texType == 0:
        fileBaseName += '_Diffuse'
    if texType == 1:
        fileBaseName += '_Normal'
    if texType == 2:
        fileBaseName += '_Roughness'
    if texType == 3:
        fileBaseName += '_Specular'

    fileBaseName = fileBaseName.lower()
        
    retFileName = ''
    for i in range(len(rFilesList)):
        fName = rFilesList[i].lower()
        iPos = fName.find(fileBaseName)
        if iPos == 0:
            retFileName = rFilesList[i]
            break
    
    if retFileName == '' and texType == 3:
        fileBaseName =  projectName + '_' + textureSetName + '_Reflection'
        fileBaseName = fileBaseName.lower()
        for i in range(len(rFilesList)):
            fName = rFilesList[i].lower()
            iPos = fName.find(fileBaseName)
            if iPos == 0:
                retFileName = rFilesList[i]
                break
        
    return retFileName
   
# ----------------------------------------------------.
# 画像を読み込み、サムネイルを保存.
# ----------------------------------------------------.
def createThumbnailImageFile (fileName, texType = 0):
    fileFullPath = EXPORT_FILE_PATH + '/' + fileName
    thumbnailFullPath = TEX_FILE_PATH + '/' + texNameList[texType]
    retName = 'none_thumb.png'         # カラのファイル名
   
    scene = xshade.scene()
    dirtyF = scene.dirty
    
    # 選択されている形状を一時保持.
    activeShapesList = xshade.scene().active_shapes
    
    scene.begin_creating()
    mImage = None
    try :
        mImage = scene.create_master_image('test')
        mImage.load_image(fileFullPath)     # この部分が重い.
        
        # サムネイル画像になるように縮小.
        small_img = mImage.image.duplicate((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), True, 32)
        small_img = mImage.image
        small_img.save(thumbnailFullPath)
        retName = texNameList[texType]
    except:    
        mImage = None

    scene.end_creating()
    if mImage != None:
        mImage.remove()     # 作業用に読み込んだマスターサーフェスは削除.
        
    # 選択をもとに戻す.
    xshade.scene().active_shapes = activeShapesList
        
    xshade.scene().dirty = dirtyF
    
    return retName

# 「project : textureSet」より、Project名とTextureSet名に分解.
projectName = ''
textureSetName = ''
str = urllib.unquote(f_projectTexName)
aList = str.split(':')

result = ''
if len(aList) == 2:
    projectName    = aList[0].strip()
    textureSetName = aList[1].strip()

    # diffuse/normal/roughness/specularの順に存在確認.
    for i in range(4):
        fName = checkImagesFile(projectName, textureSetName, i)
        if fName != '':
            retName = createThumbnailImageFile(fName, i)
            if len(result) > 0:
                result += ','
            result += retName

