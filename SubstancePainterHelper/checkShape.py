#-------------------------------------------------------------.
# 指定の形状が存在するか。.
# @param[in]  name     形状名.
#-------------------------------------------------------------.
shape = xshade.scene().get_shape_by_name(name, True)

result = 'False'
if shape != None:
  result = 'True';
