import bpy

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