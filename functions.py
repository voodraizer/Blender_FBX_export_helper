import bpy
import os


#-----------------------------------------------------------------------------------------------------------------------------
# .
#
#-----------------------------------------------------------------------------------------------------------------------------
class BlenderObject:
	"""docstring"""
	obj = None

	# Old object status.
	is_select = True
	is_visible = True
	is_render = True

	def __init__(self):
		"""Constructor"""
		pass

class CollectionObject:
	"""docstring"""
	# Collection name
	name = ""

	# Old object status.
	is_select = True
	is_visible = True
	is_render = True

	# Blender objects.
	objects = []

	def __init__(self, name):
		"""Constructor"""
		self.name = name
		pass

#-----------------------------------------------------------------------------------------------------------------------------
# .
#
#-----------------------------------------------------------------------------------------------------------------------------
class BlenderScene:
	"""docstring"""
	scene = None
	# 
	collections = []
	

	def __init__(self, scene):
		"""Constructor"""
		self.scene = scene

		pass
	
	def GetCollections(self):
		"""
		Get all collections and build hierarchical structures.
		"""

		# Get list of collections from all objects.
		#for obj in context.scene.objects:
		for c in bpy.data.collections.keys():
			coll = bpy.data.collections.get(c)

			c_obj = CollectionObject(c)
			c_obj.is_select = True
			c_obj.is_visible = True
			c_obj.is_render = True
			c_obj.objects = coll.objects

			self.collections.append(c_obj)
	
		# for col in bpy.data.collections.keys():
		# 	parent_col = GetParentCollectionRecursive(col)
		# 	print(col, " ==> ", parent_col)
			
		# 	if (parent_col == col):
		# 		# root collection
		# 		collections.append(col)
		# 	else:
				
		# 		pass
		
		# Clean all non unique lists of collections.
		
		# Build hierarchical collection.
		#PackCollectionListToHierarchy(col) 

		pass
	
# 	def GetParentCollectionRecursive(self, child_col):
# 		def GetParentCollection(child_col):
# 			# TODO надо возврать название слоя и массив с иерархией коллекций.
# 			for col in bpy.data.collections.keys():
# 				for c in bpy.data.collections.get(col).children.keys():
# 					if (child_col == c):
# 						print("                     ", child_col)
# 						return col
			
# 			return None

# 		parent_col = child_col
		
# 		while(True):
# 			tmp = GetParentCollection(parent_col)

# 			if (tmp != None): parent_col = tmp

# 			if (parent_col == child_col or tmp == None):
# 				break

# 		return parent_col

# 	def PackCollectionListToHierarchy(self, col):
# 		"""
# 		Get plane collection and build 
# 		"""
# 		length = len(col)
		
# 		if (length == 1):
# 			return [col[0], ""]
# 		if (length == 2):
# 			return [col[1], col[0]]
			
# 		tmpcollect = [col[1], col[0]]
# 		for i in range(2, length - 1):
# 			tmpcollect = [tmpcollect, col[i]]
# 			tmpcollect.reverse()
		
# 		tmpcollect = [col[length - 1], tmpcollect]
			
# 		return tmpcollect
	
# 	def GetCollectionsListFromHierarchy(self, col_hierarchy, col):
#     	collect = []
    
#     	def GetSub(sub):
# 			nonlocal collect
# 			if (not isinstance(sub, list)):
# 				collect.append(sub)
# 				return collect
				
# 			for i in sub:
# 				collect = GetSub(i)
					
# 			return collect
		
# 		GetSub(col_hierarchy)
		
# 		if (col in collect):
# 			indx = collect.index(col)
# 			return collect[:indx + 1]

# 		return None
	
# 	def GetCollectionFromObject(self, obj):

# 		pass
	
# 	def CheckIfObjInCollection(self, obj, collection):
# 		col = bpy.data.collections.get(collection)
# 		if col:
# 			for o in col.all_objects:
# 				if (o == obj):
# 					return True

# 		return False

# 	def CheckCollectionIsExportable(self, collection):
# 		is_exportable = True
# 		export_settings =  bpy.context.scene.export_helper_settings

# 		col = bpy.data.collections.get(collection)
# 		if col:
# 			# if ('_NOEXP'):
# 			# 	is_exportable = False
# 			if (col.hide_render and not export_settings.export_renderable):
# 				is_exportable = False
			
# 			print("Col: " + col.name + " Rend: " + str(col.hide_render) +  " Exp: " + str(is_exportable))
# 			print(export_settings)
# 			print("")

# 		return is_exportable

# 	def CheckObjectIsExportable(self, obj):
# 		is_exportable = True
# 		export_settings =  bpy.context.scene.export_helper_settings

# 		# Check collection.

# 		if (obj.hide_render and not export_settings.export_renderable):
# 			is_exportable = False

# 		return is_exportable


def get_parent_collection_names(collection, parent_names):
	for parent_collection in bpy.data.collections:
		if collection.name in parent_collection.children.keys():
			parent_names.append(parent_collection.name)
			get_parent_collection_names(parent_collection, parent_names)
			return


def turn_collection_hierarchy_into_path(obj):
	'''
	obj = bpy.context.view_layer.objects.active
	print(turn_collection_hierarchy_into_path(obj))
	'''
	parent_collection = obj.users_collection[0]
	parent_names      = []
	parent_names.append(parent_collection.name)
	get_parent_collection_names(parent_collection, parent_names)
	parent_names.reverse()
	return '\\'.join(parent_names)




#-----------------------------------------------------------------------------------------------------------------------------
# Fbx export settings.
#
#-----------------------------------------------------------------------------------------------------------------------------
unity_kwargs = dict(
	use_selection = True,
	use_active_collection = False,
	global_scale = 1.0,
	apply_unit_scale = True,
	apply_scale_options = 'FBX_SCALE_ALL',
	bake_space_transform = False,
	object_types = {'OTHER', 'MESH', 'EMPTY'},
	use_mesh_modifiers = True,
	use_mesh_modifiers_render = True,
	mesh_smooth_type = 'OFF',
	use_mesh_edges = False,
	use_tspace = False,
	use_custom_props = False,
	add_leaf_bones = True,
	primary_bone_axis = 'Y',
	secondary_bone_axis = 'X',
	use_armature_deform_only = False,
	armature_nodetype = 'NULL',
	bake_anim = True,
	bake_anim_use_all_bones = True,
	bake_anim_use_nla_strips = True,
	bake_anim_use_all_actions = True,
	bake_anim_force_startend_keying = True,
	bake_anim_step = 1.0,
	bake_anim_simplify_factor = 1.0,
	path_mode = 'AUTO',
	embed_textures = False,
	batch_mode = 'OFF',
	use_batch_own_dir = True,
	axis_forward = '-X',
	axis_up = 'Z'
)

#-----------------------------------------------------------------------------------------------------------------------------
# Export objects from array.
#
# exported_objects (Array) 
# {objects set 1}{objects set 2}{...}
#
# Each 'objects set' will exported in their individual file.
#-----------------------------------------------------------------------------------------------------------------------------
def ExportFbx(exported_objects, export_path, export_name):
	# Select objects.
	for sub_arr in exported_objects:
		path = export_path
		bpy.ops.object.select_all(action='DESELECT')
		
		for o in sub_arr:
			obj = o.obj
			
			# Unhide, unfreeze and select.
			obj.hide_select = False
			obj.hide_viewport = False #obj.visible_get() #bpy.ops.object.hide_view_set(unselected=False)
			obj.hide_render = False
			obj.select_set(True) #OLD obj.select = True
			#bpy.context.view_layer.objects.active = obj #OLD bpy.context.scene.objects.active = obj
	
		# Get path and name.
		path += export_name
		path += ".fbx"
	
		# Export.
		#bpy.ops.export_scene.fbx(filepath = path, use_selection=True)
		bpy.ops.export_scene.fbx(filepath = path, **unity_kwargs)

	pass

#-----------------------------------------------------------------------------------------------------------------------------
# Get collection of objects.
#
#-----------------------------------------------------------------------------------------------------------------------------
def GetAllCollection(scene):
	scene_collections = []
	
	return scene_collections

#-----------------------------------------------------------------------------------------------------------------------------
# Collect objects in the scene for further export.
#
#-----------------------------------------------------------------------------------------------------------------------------
def GetAllExported(all_objects):
	exported_objects = []

	for obj in all_objects:
		if (obj.type != 'MESH' and obj.type != 'EMPTY'):
			continue
		
		exported_obj = BlenderObject()
		exported_obj.obj = obj
		exported_obj.is_select = obj.hide_select
		exported_obj.is_visible = obj.visible_get()
		exported_obj.is_render = obj.hide_render

		exported_objects.append(exported_obj)

	pass

	return exported_objects

#-----------------------------------------------------------------------------------------------------------------------------
# Collect objects in the scene for further export.
#
# Example object naming:
# 		out_rock_wall_2b_5_LOD0
# 		out_rock_wall_2b_5_LOD0_outline
# 		out_rock_wall_2b_5_LOD1
# 		out_rock_wall_2b_5_LOD1_outline
#
# Return arrays of BlenderObjects
# [[b_obj, b_obj, b_obj], [b_obj], [b_obj, b_obj], ...]
# Each subarray will be exported in single fbx file.

def GetExportedObjectsByName(objects_array):
	# TODO
	# Учитывать флажки из вкладки геометри и скипать на основе их.

	already_exported_objects = []
	temp_already_collected = []

	export_settings =  bpy.context.scene.export_helper_settings

	for obj in objects_array:
		if (obj.type != 'MESH' and obj.type != 'EMPTY'):
			continue
		
		# Skip object by settings.
		#if (export_settings.export_freeze export_settings.export_hidden):
		#	continue

		if (obj in temp_already_collected):
			continue

		# Get objects by match name.
		temp_objects = []
  
		indx = obj.name.index("_LOD")
		if (indx == -1):
		  # Not found '_LOD'
		  continue
		#
		base_name = obj.name[0:indx]
		#print("Base: " + base_name)
			

		# Collect object with matched names.
		for sel_obj in objects_array:
			if (sel_obj in temp_already_collected):
				continue
			if (sel_obj.name.startswith(base_name)):
				#print("Base: " + base_name);
				temp_already_collected.append(sel_obj)

				exported_obj = BlenderObject()
				exported_obj.obj = sel_obj
				exported_obj.is_select = sel_obj.hide_select
				exported_obj.is_visible = sel_obj.visible_get()
				exported_obj.is_render = sel_obj.hide_render

				temp_objects.append(exported_obj)
			
		# Mark objects as exported.
		already_exported_objects.append(temp_objects)
		temp_objects = []

	pass

	return already_exported_objects

#-----------------------------------------------------------------------------------------------------------------------------
# Collect objects in the scene for further export.
#

def CheckObjectIsExportable(obj):
	is_exportable = True
	export_settings =  bpy.context.scene.export_helper_settings

	# Check collection.

	if (obj.hide_render and not export_settings.export_renderable):
		is_exportable = False
	
	if (obj.hide_get() and not export_settings.export_hidden):
		is_exportable = False
	# if (obj.visible_get() and not export_settings.export_hidden):
	# 	is_exportable = False
	
	if (obj.hide_select and not export_settings.export_freeze):
		is_exportable = False

	return is_exportable

def CheckIfObjInCollection(obj, collection):
	col = bpy.data.collections.get(collection)
	if col:
		for o in col.all_objects:
			if (o == obj):
				return True

	return False

def GetExportedObjectsFromCollection(all_objects, collections):
	exported_objects = []

	export_settings =  bpy.context.scene.export_helper_settings

	if (export_settings.export_from_hidden_collections):
		# use all collections.
		pass
	
	#bpy.context.scene.collection.children.keys()     # list of collections
	#col2 = bpy.context.scene.collection.children['Collection 2']    # get this collection

	# Select objects from active collection
	# active_col_name = bpy.context.collection.name
	#bpy.context.view_layer.active_layer_collection.name
	#bpy.context.view_layer.active_layer_collection.collection.objects
	
	# col = bpy.data.collection.get(active_col_name)
	# if col:
	# 	for obj in col.objects:
	# 		obj.select_set(True)

	for obj in all_objects:
		if (not CheckObjectIsExportable(obj)):
			continue

		for collect in collections:
			# if (not CheckCollectionIsExportable(collect)):
			# 	continue

			# Check if object in collection.
			if (CheckIfObjInCollection(obj, collect)):
				exported_obj = BlenderObject()
				exported_obj.obj = obj
				exported_obj.is_select = obj.hide_select
				exported_obj.is_visible = not obj.hide_get() #obj.visible_get()
				exported_obj.is_render = obj.hide_render

				exported_objects.append(exported_obj)

				#print("Obj: " + obj.name + " Vis: " + str(obj.hide_get()))
	pass

	return exported_objects


#
def GetShadowAndOutlineObjects(all_objects):
	collected_objects = []
	collected_objects.append([])
	
	for obj in all_objects:
		if (obj.type == 'MESH' and obj.name.find("_shadow") != -1): # and IsObjectInVisibleLayer(temp_scene, obj)):
			# Shadow objects.
			collected_obj = BlenderObject()
			collected_obj.obj = obj
			collected_obj.is_select = obj.hide_select
			collected_obj.is_visible = obj.visible_get()
			collected_obj.is_render = obj.hide_render

			collected_objects[0].append(collected_obj)

		if (obj.type == 'MESH' and obj.name.find("_outline") != -1): # and IsObjectInVisibleLayer(temp_scene, obj)):
			# Outline object.
			collected_obj = BlenderObject()
			collected_obj.obj = obj
			collected_obj.is_select = obj.hide_select
			collected_obj.is_visible = obj.visible_get()
			collected_obj.is_render = obj.hide_render

			collected_objects[0].append(collected_obj)

	return collected_objects

# def BatchFbxExportByName(self, export_objects):
# 	# exports each selected object into its own file

# 	# export to blend file location
# 	basedir = os.path.dirname(bpy.data.filepath)

# 	if not basedir:
# 		raise Exception("Blend file is not saved")

# 	view_layer = bpy.context.view_layer

# 	obj_active = view_layer.objects.active
# 	selection = bpy.context.selected_objects

# 	bpy.ops.object.select_all(action='DESELECT')

# 	for obj in selection:

# 		obj.select_set(True)

# 		# some exporters only use the active object
# 		view_layer.objects.active = obj

# 		name = bpy.path.clean_name(obj.name)
# 		fn = os.path.join(basedir, name)

# 		bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True)

# 		# Can be used for multiple formats
# 		# bpy.ops.export_scene.x3d(filepath=fn + ".x3d", use_selection=True)

# 		obj.select_set(False)

# 		print("written:", fn)


# 		view_layer.objects.active = obj_active

# 		for obj in selection:
# 			obj.select_set(True)

#--------------------------------------------------------------------------------------------------
# Scene.
#--------------------------------------------------------------------------------------------------
def RestoreScene(exported_objects):
	# Restore visible, selected, renderable objects.
	for arr in exported_objects:
		for o in arr:
			o.obj.hide_select = o.is_select
			o.obj.hide_set(not o.is_visible) #o.obj.hide_viewport = o.is_visible
			o.obj.hide_render = o.is_render

	# Restore collections visibility.

	# Restore objects transform.
	
	pass

def UnhideAndUnfreezeAll(exported_objects):
	# Unhide objects.
	#bpy.ops.object.hide_view_clear() # ::FAKE
	for o in exported_objects:
		o.obj.hide_select = False
		o.obj.hide_set(False)
		o.obj.hide_render = False

	# Unhide collections.

	pass

def UnhideAndUnfreezeFrom(scene_object):
	#bpy.ops.object.hide_view_clear() # ::FAKE
	
	pass

#--------------------------------------------------------------------------------------------------
# Find exported filename.
# detect visible empty object starts with '_export_' and use one for export name.
#--------------------------------------------------------------------------------------------------
def GetExportFilename():
	if (bpy.data.filepath == ''):
		return None
	
	for ob_base in bpy.data.objects:
		if (ob_base.type == 'EMPTY' and ob_base.is_visible(bpy.context.scene) and ob_base.name.startswith("_export_")):
			# remove '_export_' from file name
			filename = ob_base.name[8: len(ob_base.name)]
			export_file = filename + ".fbx"
			return export_file
	
	return None

def GetExportName():
	if (bpy.data.filepath == ''):
		return None
	
	for ob_base in bpy.data.objects:
		if (ob_base.type == 'EMPTY' and ob_base.is_visible(bpy.context.scene) and ob_base.name.startswith("_export_")):
			# remove '_export_' from dummy name
			export_name = ob_base.name[8: len(ob_base.name)]
			return export_name
	
	return None

#--------------------------------------------------------------------------------------------------
# Find project path (root of art repository).
#--------------------------------------------------------------------------------------------------
def GetProjectPath():
	if (bpy.data.filepath == ''):
		return None
	
	blend_file_path = os.path.dirname(bpy.data.filepath)
	index = blend_file_path.lower().find("models")
	if (index != -1):
		project_path = blend_file_path[0:index]
	
		return project_path
	else:
		#print("Not found project path.")
		pass
	
	return None

#--------------------------------------------------------------------------------------------------
# Find local path (relative root of art repository).
#--------------------------------------------------------------------------------------------------
def GetLocalPath():
	if (bpy.data.filepath == ''):
		return None
	
	blend_file_path = os.path.dirname(bpy.data.filepath)
	index = blend_file_path.lower().find("models")
	if (index != -1):
		export_path = blend_file_path[index:len(blend_file_path)]
	
		return export_path
	else:
		#print("Not found local path.")
		pass
	
	return None

#--------------------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------------------
def SaveSettings():
	
	pass

def CleanScene(temp_scene):#, cur_scene):
	bpy.ops.object.select_all(action='DESELECT')
	selection = temp_scene.objects
	
	for obj in selection:
		obj_data = obj.data
		
		#obj.select = True
		#temp_scene.objects.active = obj
		temp_scene.objects.unlink(obj)
		
		if (obj.users > 0):
			obj.user_clear()
		
		#bpy.ops.object.delete()
		bpy.data.objects.remove(obj)
		
		if (obj_data.users > 0):
			obj_data.user_clear()
		else:
			bpy.data.meshes.remove(obj_data)

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
# Collect object for export.
#--------------------------------------------------------------------------------------------------

def IsObjectCollision(obj_name):
	if (obj_name.startswith("UCX_") or obj_name.startswith("UBX_") or obj_name.startswith("USP_")):
		return True
	
	return False

def Collect_collisions(temp_scene):
	collisions = []
	
	for obj in temp_scene.objects:
		if (IsObjectCollision(obj.name)):# and obj.name.find(self.export_name) != -1):
			collisions.append(obj)
	
	return collisions

def Collect_objects(temp_scene):
	objects = []
	
	for obj in temp_scene.objects:
		if (not IsObjectCollision(obj.name)):
			objects.append(obj)
	
	return objects

def CollectTempObjects(fbx_helper, cur_scene, export_name):
		temp_objects = []
		
		for obj in cur_scene.objects:
			# skip objects in hidden layers
			if (not IsObjectInVisibleLayer(cur_scene, obj) or obj.hide_render or obj.name.startswith('_export_')):
				continue
			
			if (IsObjectCollision(obj.name)):
				if (not fbx_helper.export_colliders):
					continue
				if (obj.name.find(export_name) == -1):
					# skip other collisions
					continue
			else:
				# detect if object not need to be exported
				if (obj.type != 'MESH' and obj.type != 'CURVE'):
					continue
				if (obj.hide and (not fbx_helper.export_hidden)):
					continue
				if (obj.hide_select and (not fbx_helper.export_freeze)):
					continue
				#if (obj.hide_render or obj.name.startswith('_export_') ): #or (not obj.is_visible(cur_scene))):
				#	continue
			
			if (fbx_helper.ignore_materials):
				# TODO: assing default mat
				pass
			
			# FAKE. 
			UseMaterialNodes(obj, False)
			
			temp_objects.append(obj)
		
		return temp_objects

def CollectTempObjectsByMat(fbx_helper, cur_scene, export_name):
		temp_objects = []
		
		for obj in cur_scene.objects:
			if (IsObjectCollision(obj.name)):
				if (not fbx_helper.export_colliders):
					continue
				if (obj.name.find(export_name) == -1):
					# skip other collisions
					continue
			else:
				# detect if object not need to be exported
				if (obj.type != 'MESH' and obj.type != 'CURVE'):
					continue
				if (obj.hide and (not fbx_helper.export_hidden)):
					continue
				if (obj.hide_select and (not fbx_helper.export_freeze)):
					continue
				if (obj.hide_render or obj.name.startswith('_export_') or (not obj.is_visible(cur_scene))):
					continue
			
			temp_objects.append(obj)
		
		if (fbx_helper.ignore_materials):
			return temp_objects
		
		if (not fbx_helper.sort_materials):
			return temp_objects
		
		# sort collected objects by materials (MatName_skin00, MatName_skin01, MatName_skin02 ...)
		#print("\n\n\n#######################################")
		
		# get all material names and material names contain "skin"
		mat_names = []
		mat_with_skin_substr = []
		for obj in temp_objects:
			if (len(obj.material_slots) > 0):
				for m in obj.material_slots:
					if (not m.name in mat_names):
						mat_names.append(m.name)
						
						s_arr = m.name.split("skin")
						if (len(s_arr) > 1):
							s = "skin" + s_arr[len(s_arr) - 1]
							mat_with_skin_substr.append(s)
		
		mat_with_skin_substr.sort(reverse = True)
		
		# get material names with "skin"
		for indx in range(len(mat_with_skin_substr)):
			sub = mat_with_skin_substr[indx]
			for m in mat_names:
				if (m.count(sub) == 1):
					mat_with_skin_substr[indx] = m
					break
		
		# get material names without "skin"
		mat_names_others = []
		for m in mat_names:
			if (not m in mat_with_skin_substr):
				mat_names_others.append(m)
		
		mat_names_others.sort(reverse = True)
		
		# append
		mat_names = mat_names_others + mat_with_skin_substr
		
		# reorder object by materials order in array
		temp_objects_copy = temp_objects.copy()
		temp_objects.clear()
		
		for mat in mat_names:
			for obj in temp_objects_copy:
				if (len(obj.material_slots) > 0):
					# TODO: как быть с мультиматериалами (в какой последовательности добавлять объекты ?)
					if (obj.material_slots[0].name == mat):
						temp_objects.append(obj)
		
		#print(mat_names)
		#print(mat_with_skin_substr)
		#print(mat_names_others)
		
		return temp_objects

#--------------------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------------------
def Collapse_collisions(temp_scene, export_name):
	# find collisions and merge
	bpy.ops.object.select_all(action='DESELECT')
	
	collisions = Collect_collisions(temp_scene)
	
	if (len(collisions) > 0):
		for obj in collisions:
			obj.hide_select = False
			obj.hide = False
			#obj.select = True
			#temp_scene.objects.active = obj
		
		if (len(collisions) > 1):
			bpy.ops.object.select_all(action='TOGGLE')
			#print("Selected: " + str(bpy.context.selected_objects))
		
			#collisions[0].select = True
			temp_scene.objects.active = collisions[0]
			bpy.ops.object.join()

		collisions[0].name = "UCX_" + export_name + "_export"

def Collapse_objects(temp_scene, export_name):
	bpy.ops.object.select_all(action='DESELECT')
	
	objects = Collect_objects(temp_scene)
	
	for obj in objects:
		obj.hide_select = False
		obj.hide = False
	
	if (len(objects) > 1):
		bpy.ops.object.select_all(action='TOGGLE')
	
		temp_scene.objects.active = objects[0]
		#objects[0].select = True
		bpy.ops.object.join()
	
	temp_scene.objects.active = objects[0]
	#objects[0].select = True
	temp_scene.objects.active.name = export_name + "_export"

#--------------------------------------------------------------------------------------------------
# .
#--------------------------------------------------------------------------------------------------
def SincAllObjects(temp_scene):
	objs = Collect_objects(temp_scene)
	
	for o in objs:
		#Collapse_vc_layers(o)
		Create_default_vc_layers(o)
	
	
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
