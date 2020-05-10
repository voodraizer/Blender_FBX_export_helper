import bpy


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
	import os

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
	import os

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

