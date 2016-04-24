# ------------------------------------------------------------------.
# Substance Painterのテクスチャを読み込み、マスターサーフェスに割り当て.
#
# @param[in]  f_filePath        exportテクスチャのあるパス (string).
# @param[in]  f_projectTexName 「project : textureSet」の値(string).
# @param[in]  f_updateMasterImage マスターイメージを上書きする場合はtrue.
# @param[in]  f_updateMasterSurface  マスターサーフェスを上書きする場合はtrue.
# @param[in]  f_textureGamma       マスターイメージのテクスチャの逆ガンマ.  
# ------------------------------------------------------------------.
import urllib
import os
import os.path

# Exportファイルのあるパス.
EXPORT_FILE_PATH = urllib.unquote(f_filePath)

# ディレクトリ中のファイル一覧を取得.
dirPath = urllib.unquote(f_filePath)
rFilesList = get_files_name(dirPath)

updateMasterImageF = False
if f_updateMasterImage == '1':
    updateMasterImageF = True

updateMasterSurfaceF = False
if f_updateMasterSurface == '1':
    updateMasterSurfaceF = True

textureGammaF = False
if  f_textureGamma == '1':
    textureGammaF = True
    
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
# テクスチャを読み込み、マスターサーフェスに反映.
# ----------------------------------------------------.
def loadTextureFile (texFileName, texType = 0):
    if texFileName == None or texFileName == '':
        return None
    
    # フルパス名.
    absFileName = EXPORT_FILE_PATH + '/' + texFileName
    
    # 同一ファイル名がすでに存在するかチェック.
    mImage = None
    if updateMasterImageF:
        mImage = xshade.scene().get_shape_by_name(texFileName, False)

    xshade.scene().begin_creating()
    if mImage == None:
        mImage = xshade.scene().create_master_image(texFileName)
        
    name = ''
    try:
        mImage.load_image(absFileName)
        name = absFileName

        # テクスチャの逆ガンマの指定.
        if texType == 0:
            if textureGammaF:
                mImage.gamma = 0.4545
            else: 
                mImage.gamma = 1.0
        
    except:
        name = ''
    xshade.scene().end_creating()

    if name == None or name == '':
        return None
    return mImage.image    

# ----------------------------------------------------.
#  同一マスターサーフェスを検索.
# ----------------------------------------------------.
def findMasterSurface (masterSurfaceName):
    # マスターサーフェスパートを取得
    rootShape = xshade.scene().shape
    if rootShape.has_son == False:
        return None

    masterSurfacePart = None
    s = rootShape.son
    while s.has_bro:
        s = s.bro
        if s.type == 2:     # パート.
            if s.part_type == 100:      # マスターサーフェスパート.
                masterSurfacePart = s
                break
                
    if masterSurfacePart == None:
        return None
    
    # 同一マスターサーフェス名が存在するか調べる.
    masterSurface = None
    s = masterSurfacePart.son
    while s.has_bro:
        s = s.bro
        if s.name == masterSurfaceName:
           masterSurface = s
           break
           
    return masterSurface
    
# ----------------------------------------------------.
# Substance Painterの表現を近似したマスターサーフェスの作成.
# 参考 : http://qiita.com/ft-lab/items/98cd34a7a9379d64e187
# ----------------------------------------------------.
def createMasterSurface (projectName, textureSetName, diffuseImage, normalImage, roughnessImage, specularImage):
    masterSurfaceName = textureSetName
    
    # 同一ファイル名がすでに存在するかチェック.
    masterSurface = None
    if updateMasterSurfaceF:
        masterSurface = findMasterSurface(masterSurfaceName)
    
    successF = False
    xshade.scene().begin_creating()
    try:
        # 基本情報を指定.
        if masterSurface == None:
            masterSurface = xshade.scene().create_master_surface(masterSurfaceName)
        masterSurface.surface.diffuse = 1.0
        masterSurface.surface.diffuse_color = [1, 1, 1]
        masterSurface.surface.highlight = 0.0
        masterSurface.surface.highlight_size = 0.0
        masterSurface.surface.reflection = 1.0
        masterSurface.surface.roughness = 1.5
        masterSurface.surface.fresnel_reflection = 0.68
        
        # テクスチャのマッピングレイヤを指定 (7層分).
        masterSurface.surface.append_mapping_layer()
        mLayer = masterSurface.surface.mapping_layer(0)
        mLayer.blend_mode = 0           # 通常.
        mLayer.pattern = 14             # イメージ.
        mLayer.type = 0                 # 拡散反射.
        mLayer.flip_color = False       # 反転フラグ.
        mLayer.blur = True              # スムーズ.
        mLayer.image = diffuseImage
        
        masterSurface.surface.append_mapping_layer()
        mLayer = masterSurface.surface.mapping_layer(1)
        mLayer.blend_mode = 4           # 乗算.
        mLayer.pattern = 14             # イメージ.
        mLayer.type = 0                 # 拡散反射.
        mLayer.flip_color = True        # 反転フラグ.
        mLayer.blur = True              # スムーズ.
        mLayer.image = specularImage

        masterSurface.surface.append_mapping_layer()
        mLayer = masterSurface.surface.mapping_layer(2)
        mLayer.blend_mode = 0           # 通常.
        mLayer.pattern = 14             # イメージ.
        mLayer.type = 21                # 法線.
        mLayer.flip_color = False       # 反転フラグ.
        mLayer.blur = True              # スムーズ.
        mLayer.image = normalImage

        masterSurface.surface.append_mapping_layer()
        mLayer = masterSurface.surface.mapping_layer(3)
        mLayer.blend_mode = 0           # 通常.
        mLayer.pattern = 14             # イメージ.
        mLayer.type = 3                 # 反射.
        mLayer.flip_color = False       # 反転フラグ.
        mLayer.blur = True              # スムーズ.
        mLayer.image = specularImage

        masterSurface.surface.append_mapping_layer()
        mLayer = masterSurface.surface.mapping_layer(4)
        mLayer.blend_mode = 4           # 乗算.
        mLayer.pattern = 14             # イメージ.
        mLayer.type = 3                 # 反射.
        mLayer.flip_color = True        # 反転フラグ.
        mLayer.blur = True              # スムーズ.
        mLayer.image = roughnessImage

        masterSurface.surface.append_mapping_layer()
        mLayer = masterSurface.surface.mapping_layer(5)
        mLayer.blend_mode = 0           # 通常.
        mLayer.pattern = 14             # イメージ.
        mLayer.type = 12                # 荒さ.
        mLayer.flip_color = True        # 反転フラグ.
        mLayer.blur = True              # スムーズ.
        mLayer.image = roughnessImage

        masterSurface.surface.append_mapping_layer()
        mLayer = masterSurface.surface.mapping_layer(6)
        mLayer.blend_mode = 2           # 加算.
        mLayer.pattern = 14             # イメージ.
        mLayer.type = 12                # 荒さ.
        mLayer.flip_color = True        # 反転フラグ.
        mLayer.blur = True              # スムーズ.
        mLayer.image = specularImage
        
        successF = True
    except:
        successF = False
        
    xshade.scene().end_creating()
    return successF

# 「project : textureSet」より、Project名とTextureSet名に分解.
projectName = ''
textureSetName = ''
str = urllib.unquote(f_projectTexName)
aList = str.split(':')

result = ''
if len(aList) == 2:
    projectName    = aList[0].strip()
    textureSetName = aList[1].strip()

    # diffuse/normal/roughness/specularの順にファイルを読み込み、マスターサーフェスに割り当て.
    # Diffuseテクスチャ画像の読み込み.
    fName = checkImagesFile(projectName, textureSetName, 0)
    diffuseImage = loadTextureFile(fName, 0)
            
    # Normalテクスチャ画像の読み込み.
    fName = checkImagesFile(projectName, textureSetName, 1)
    normalImage = loadTextureFile(fName, 1)

    # Roughnessテクスチャ画像の読み込み.
    fName = checkImagesFile(projectName, textureSetName, 2)
    roughnessImage = loadTextureFile(fName, 2)

    # Specularテクスチャ画像の読み込み.
    fName = checkImagesFile(projectName, textureSetName, 3)
    specularImage = loadTextureFile(fName, 3)
        
    # マスターサーフェスの作成.
    if diffuseImage != None and normalImage != None and roughnessImage != None and specularImage != None:
        if createMasterSurface(projectName, textureSetName, diffuseImage, normalImage, roughnessImage, specularImage):
            print "create master surface [" + textureSetName + "]"
       
