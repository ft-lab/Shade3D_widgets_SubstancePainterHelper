あ# Shade3D_widgets_SubstancePainterHelper
SubstancePainterHelper (Shade 3D widgets)

## 概要

Substance Painterで出力したテクスチャ（Diffuse/Normal/Roughness/Specularの4枚）をShade 3DにインポートするScriptです。
Shade 3D ver.14または15 Basic/Standard/Professional以降で動作します。

Substance PainterもしくはSubstance Painter 2では、テクスチャのエクスポート時に「Shade 3D」のConfigで出力するようにしてください。


## 使い方

ダウンロードしたSubstancePainterHelperディレクトリを、Shade 3Dのユーザのドキュメントディレクトリ下の
Shade 3D ver.15/widgets にコピーし、Shade 3Dを起動してください。

メインメニューの「スクリプト」-「Substance Painter Helper」を選択すると、Substance Painter Helperウィンドウが表示されます。

「画像ファイル指定」ボタンを押して、Substance Painterで出力したディレクトリ内のファイルを1つ選択してください。
指定ファイルのあるディレクトリの要素がリストボックスに表示されます。

「Project名 : TextureSet名」が列挙されます。それぞれのTextureSetに対して4枚の「Diffuse/Normal/Roughness/Specular」が存在します。

リストボックスで要素を選択し「選択テクスチャを読込」ボタンを押すと、選択したテクスチャだけ読み込まれます。
このときに4枚のテクスチャの読み込みとマスターサーフェスが作成されます。
マスターサーフェス名はTextureSet名が使用されます。

「すべてのテクスチャを読込」ボタンを押すと、リスト内にあるすべてのテクスチャが読み込まれ、マスターサーフェスが生成されます。

「マスターイメージの上書き」チェックボックスをOnにしておくと、同一マスターイメージ名がある場合は上書きします。

「マスターサーフェスの上書き」チェックボックスをOnにしておくと、同一マスターサーフェスがある場合は上書きします。

「テクスチャの逆ガンマ補正」チェックボックスをOnにしておくと、テクスチャを読み込んだ際に、ガンマ値0.4545にします。
シーン要素をリニアにしたい場合にチェックしてください。

## 表面材質のマッピングレイヤ配置ルール

「Substance Painterの使い方 (4) テクスチャのエクスポート編」

http://qiita.com/ft-lab/items/98cd34a7a9379d64e187

に書いている配置ルールを使ってます。

## ライセンス

改変自由です。
ご自由にお使いくださいませ。






