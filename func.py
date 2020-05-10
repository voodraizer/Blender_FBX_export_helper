import bpy
import os




#--------------------------------------------------------------------------------------------------
# Create default material.
#--------------------------------------------------------------------------------------------------
# def CreateMaterial(mat_name):
# 	mat = bpy.data.materials.new(mat_name)
# 	col = [1, 1, 1]
# 	mat.diffuse_color = col
# 	#mat.use_face_texture = True # in case the uninitated user wants a quick rendering
	
# 	return mat

# def create_default_material(obj):
# 	mat = CreateMaterial("no_mat")
	
# 	if (len(obj.data.materials) == 0):
# 		new_mesh.materials.append(mat)
# 	else:
# 		for m in range(0, len(obj.data.materials)):
# 			#obj.data.materials[m] = None
# 			obj.data.materials[m] = mat

# def UseMaterialNodes(obj, use_nodes):
# 	# Фбх не хочет экспортить нодовый материал цайкласа. Надо его конвертить в блендеровский без нод.
# 	#mats = bpy.data.materials
# 	#for cmat in mats:
# 	#	cmat.use_nodes = False
	
# 	if (len(obj.data.materials) == 0):
# 		pass
# 	else:
# 		for m in range(0, len(obj.data.materials)):
# 			obj.data.materials[m].use_nodes = use_nodes

def Delete_all_materials(obj):
	obj.data.materials.clear()
    
#--------------------------------------------------------------------------------------------------
# UVs tool.
#--------------------------------------------------------------------------------------------------
# def Uvs_rearrange(obj, uvs_order = ["UVMap", "UVMap_Decal", "UVMap_DecalAlpha", "UVMap_Atlas"]):
# 	if (obj.type != 'MESH'):
# 		return
	
# 	# delete unexpected uv maps
# 	for uv in obj.data.uv_textures.keys():
# 		if (uv not in uvs_order):
# 			obj.data.uv_textures.remove(obj.data.uv_textures[uv])
	
# 	i = 0
# 	for uv in uvs_order:
# 		if (len(obj.data.uv_textures) > i and obj.data.uv_textures[i].name == uv):
# 			i += 1
# 			continue
		
# 		# found 
# 		if (len(obj.data.uv_textures) <= i or obj.data.uv_textures.find(uv) == -1):
# 			# need create new uv
# 			newuvmap = obj.data.uv_textures.new()
# 			newuvmap.name = uv
			
# 			# move all uvs to (0, 0)
# 			for loop in obj.data.loops :
# 				#obj.data.uv_layers.active.data[loop.index].uv = (0, 0)
# 				obj.data.uv_layers[uv].data[loop.index].uv = (0, 0)
				
# 		else:
# 			# make copy
# 			indx = obj.data.uv_textures.find(uv)
# 			obj.data.uv_textures.active_index = indx
			
# 			obj.data.uv_textures[indx].name = uv + "_copy_del"
			
# 			newuvmap = obj.data.uv_textures.new()
# 			newuvmap.name = uv
			
# 		i += 1
	
# 	# delete duplicate uv maps
# 	for uv in obj.data.uv_textures.keys():
# 		if (uv.find("_copy_del") != -1):
# 			obj.data.uv_textures.remove(obj.data.uv_textures[uv])

# def Delete_uvs_except_first(obj):
# 	if (obj.type != 'MESH'):
# 		return
	
# 	num = len(obj.data.uv_textures)
# 	if (num == 0):
# 		return
	
# 	uv_tex = obj.data.uv_textures.keys()
# 	for uv in uv_tex[1:]:
# 		obj.data.uv_textures.remove(layer = obj.data.uv_textures[uv])
	
def Delete_all_uvs(obj):
	if (obj.type != 'MESH'):
		return
	
	if (len(obj.data.uv_layers) == 0):
		return

	uvs = obj.data.uv_layers.keys()
	for uv in uvs:
		obj.data.uv_layers.remove(layer = obj.data.uv_layers[uv])

#--------------------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------------------
def Set_all_smooth(obj):
	#bpy.context.view_layer.objects.active = obj
	#bpy.ops.object.shade_smooth()
	
	obj.data.use_auto_smooth = True
	obj.data.auto_smooth_angle = 3.14159 # angle = 180

	for f in obj.data.polygons:
		f.use_smooth = True

	# Clean hard edges.
	# bpy.ops.object.editmode_toggle()
	# # bpy.ops.mode.edge()
	# bpy.ops.mode.object()
	# # bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
	# bpy.ops.mesh.select_all(action='SELECT')
	# bpy.ops.mesh.mark_sharp(clear=True)
	# bpy.ops.object.editmode_toggle()
	# bpy.ops.mode.object()
	for edge in obj.data.edges:
		edge.use_edge_sharp = False



#--------------------------------------------------------------------------------------------------
# Detect if object in visible layer.
#--------------------------------------------------------------------------------------------------
def IsObjectInVisibleLayer(scene, obj):
		#return obj.is_visible(scene) # DONT WORK
		objectLayer = [i for i in range(len(obj.layers)) if obj.layers[i] == True]
		return scene.layers[objectLayer[0]]
		
#--------------------------------------------------------------------------------------------------
# Find all uv names from objects.
#--------------------------------------------------------------------------------------------------
def FindUVNames():
	
	pass

#--------------------------------------------------------------------------------------------------
# Vertex color.
#
# Скрипт объединяет цвет из вертекс-колор слоёв в один слой по формуле: new_RGB = (vc_layer_R[0], vc_layer_B[1], vc_layer_B[3]), т.е.
# берёт значение красного канала цвета в красном вертекс-колор слое, зелёного в зелёном слое и т.д. и объеденяет их.
# Имеют значения только оттенки серого в диапазоне [0, 1], поэтому цвета в вертекс-колор слоях могут быть только градациями серого.
# TODO: Для экспорта альфы необходимо модифицированная версия fbx экспортёра
#
# Слои должны иметь стандартные названия: Col_R, Col_G, Col_B, Col_A.
# Если слоя нет, то соответствующая компонента цвета в результирующем цвете будет равна 0 (для альфы - 1 ???).
# После выполнения скрипта слои удаляются (TODO: что если делать результирующий слой активным - тестировать на экспорт).
#--------------------------------------------------------------------------------------------------
# def Create_default_vc_layers(obj):
# 	if (obj.data.vertex_colors.find("Col_RGB") == -1):
# 		obj.data.vertex_colors.new("Col_RGB")
# 	if (obj.data.vertex_colors.find("Col_R") == -1):
# 		obj.data.vertex_colors.new("Col_R")
# 	if (obj.data.vertex_colors.find("Col_G") == -1):
# 		obj.data.vertex_colors.new("Col_G")
# 	if (obj.data.vertex_colors.find("Col_B") == -1):
# 		obj.data.vertex_colors.new("Col_B")
# 	# if (obj.data.vertex_colors.find("Col_A") == -1):
# 		# obj.data.vertex_colors.new("Col_A")

# def Delete_default_vc_layers(obj):
# 	if (obj.data.vertex_colors.find("Col_RGB") != -1):
# 		cl = obj.data.vertex_colors["Col_RGB"]
# 		obj.data.vertex_colors.remove(cl)
# 	if (obj.data.vertex_colors.find("Col_R") != -1):
# 		cl = obj.data.vertex_colors["Col_R"]
# 		obj.data.vertex_colors.remove(cl)
# 	if (obj.data.vertex_colors.find("Col_G") != -1):
# 		cl = obj.data.vertex_colors["Col_G"]
# 		obj.data.vertex_colors.remove(cl)
# 	if (obj.data.vertex_colors.find("Col_B") != -1):
# 		cl = obj.data.vertex_colors["Col_B"]
# 		obj.data.vertex_colors.remove(cl)
# 	# if (obj.data.vertex_colors.find("Col_A") != -1):
# 		# cl = obj.data.vertex_colors["Col_A"]
# 		# obj.data.vertex_colors.remove(cl)

# def Make_RGB_layer_as_active(obj):
# 	if (obj.data.vertex_colors.find("Col_RGB") != -1):
# 		# make layer active
# 		obj.data.vertex_colors["Col_RGB"].active = True
# 		obj.data.vertex_colors["Col_RGB"].active_render = True

# def Fill_vc_layer(obj, vc_layer, color = (0.0, 0.0, 0.0)):
# 	for d in vc_layer.data:
# 		d.color = color

# def Collapse_vc_layers(active_obj):

# 	if (active_obj.data.vertex_colors.find("Col_RGB") == -1):
# 		# not found layer Col_RGB.
# 		#self.report({''}, "Not found 'Col_RGB' vertex color layer.")
# 		Create_default_vc_layers(active_obj)
# 		pass
		
# 	# get vertex color layers data
# 	data_RGB = None
# 	data_R = None
# 	data_G = None
# 	data_B = None
# 	#data_A = None
# 	if (active_obj.data.vertex_colors.find("Col_RGB") != -1):
# 		# reset default color
# 		Fill_vc_layer(active_obj, active_obj.data.vertex_colors["Col_RGB"], color = (0.0, 0.0, 0.0))
# 		data_RGB = active_obj.data.vertex_colors["Col_RGB"].data
# 	if (active_obj.data.vertex_colors.find("Col_R") != -1):
# 		data_R = active_obj.data.vertex_colors["Col_R"].data
# 	if (active_obj.data.vertex_colors.find("Col_G") != -1):
# 		data_G = active_obj.data.vertex_colors["Col_G"].data
# 	if (active_obj.data.vertex_colors.find("Col_B") != -1):
# 		data_B = active_obj.data.vertex_colors["Col_B"].data
# 	#if (active_obj.data.vertex_colors.find("Col_A") != -1):
# 	#	data_A = active_obj.data.vertex_colors["Col_A"].data

# 	# check for errors
# 	if (active_obj.data.vertex_colors.find("Col_RGB") != 0):
# 		# layer Col_RGB must be first.
# 		pass
# 	if (data_R == None and data_G == None and data_B == None):# and data_A == None):
# 		# nothing to copy
# 		pass

# 	# copy vertex color
# 	for indx in range(len(data_RGB)):
# 		colorR = 0
# 		colorG = 0
# 		colorB = 0
# 		#colorA = 1
		
# 		# TODO: выдаёт ошибку при первом запуске, про повторном не выдаёт.
# 		if (data_R != None):
# 			colorR = data_R[indx].color[0]
# 		if (data_G != None):
# 			colorG = data_G[indx].color[1]
# 		if (data_B != None):
# 			colorB = data_B[indx].color[2]
# 		#if (data_A != None):
# 		#	colorA = data_A[indx].color[0]
# 			# # Add alpha color (from uv_bake_texture_to_vcols.py)
# 			# a_inverted = 1 - a
# 			# alpha_color = context.scene.uv_bake_alpha_color
# 			# col_result = (col_result[0] * a + alpha_color[0] * a_inverted,
# 						  # col_result[1] * a + alpha_color[1] * a_inverted,
# 						  # col_result[2] * a + alpha_color[2] * a_inverted)

# 			# vertex_colors.data[loop].color = col_result
		
# 		data_RGB[indx].color = (colorR, colorG, colorB)
		
# 		#print(indx, ": ", data_RGB[indx].color)

# 	# update mesh data
# 	#active_obj.data.update()
# 	bpy.context.scene.update()

# 	# delete old vertex color layers
# 	#Delete_default_vc_layers(active_obj)

# 	Make_RGB_layer_as_active(active_obj)

def Delete_all_vcols(obj):
	if (obj.type != 'MESH'):
		return
		
	vcols = obj.data.vertex_colors.keys()
	for vc in vcols:
		obj.data.vertex_colors.remove(layer = obj.data.vertex_colors[vc])
	
	
#--------------------------------------------------------------------------------------------------
# Find visible armature.
#--------------------------------------------------------------------------------------------------
def FindArmatureObject():

	#mesh_objects = [o for o in context.selected_objects if o.type == 'MESH']
	#obj.find_armature(
	#event.type in mouse_keys
	
	armObj = None
	for obj in bpy.context.scene.objects:
		if (obj.type == 'ARMATURE' and obj.is_visible(bpy.context.scene)):
			#for modifier in mesh_object.modifiers:
				#if modifier.type == 'ARMATURE':
			armObj = obj
			break
	return armObj

def GetKeyframesInAction(action):
	scene = bpy.context.scene
	keyframeTimes = []
	temp = set()
	for fCurve in action.fcurves:
		for keyframe in fCurve.keyframe_points:
			if keyframe.co[0] < scene.frame_start:
				temp.add(scene.frame_start)
			elif keyframe.co[0] > scene.frame_end:
				temp.add(scene.frame_end)
			else:
				temp.add(int(keyframe.co[0]))
	
	for i in temp:
		keyframeTimes.append(i)
	keyframeTimes.sort()
	
	return keyframeTimes

#--------------------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------------------
def FindArmatureActions(obj):
	animActions = None
	if (not obj or obj.type != 'ARMATURE'):
		return None
	if (obj.animation_data is None):
		return None
	#obj.animation_data.action
	animActions = bpy.data.actions
	
	return animActions

#--------------------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------------------
def StripName(Name):
    
	def ReplaceSet(String, OldSet, NewChar):
		for OldChar in OldSet:
			String = String.replace(OldChar, NewChar)
		return String

	import string

	NewName = ReplaceSet(Name, string.punctuation + " ", "_")
	return NewName
