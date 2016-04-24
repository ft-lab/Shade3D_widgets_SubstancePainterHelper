# ---------------------------------------------------.
# 指定のディレクトリ内のファイルを取得し、
# project_textureSet_Diffuse、project_textureSet_Normal、project_textureSet_Roughness、project_textureSet_Specular
# の4つより、「project : textureSet」のリストとして取得.
# 
# @param[in]  f_filePath      exportテクスチャのあるパス (string).
# ---------------------------------------------------.
import urllib

# ディレクトリ中のファイル一覧を取得.
dirPath = urllib.unquote(f_filePath)
rFiles = get_files_name(dirPath)

# 「ProjectName:TextureSetName」のリストを取得.
pList = []
for i in range(len(rFiles)):
    # ファイル名より、prjectNameとTextureSet名を取得.
    name = get_projectTextureName(rFiles[i])
    if name != None and name  != '':
        if pList.count(name) == 0:
            pList.append(name)

# aaa,bbb,ccc,ddd  のように連結したテキストにする.
result = ''
for i in range(len(pList)):
    if len(result) > 0:
        result += ','
    result += pList[i]
