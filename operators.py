
# <pep8 compliant>

import bpy
from bpy.types import Operator
from bpy.props import StringProperty, BoolProperty
from mathutils import Vector


from fbx_export_helper.functions import *


# -----------------------------------------------------------------------------------------
# 
# -----------------------------------------------------------------------------------------
class ExportHelper_OT_ExportByName(Operator):
	"""Description"""
	bl_idname = "scene.eh_export_by_name"
	bl_label = "Export by name"

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		export_settings =  bpy.context.scene.export_helper_settings

		all_objects = context.scene.objects
		#ExportBatchHelperOperator(self, context, all_objects)

		#exported_objects = CollectAllExported(all_objects)
		exported_objects = CollectExportedObjectsByName(all_objects)
		#exported_objects = CollectShadowAndOutlineObjects(all_objects)

		print(exported_objects)

		# for o in all_objects:
		# 	o.hide_select = True
		# 	o.hide_viewport = True
		# 	o.hide_render = True

		# export_name = ''
		# indx = obj.name.index("_LOD")
		# if (indx != -1):
		# 	export_name = obj.name[0:indx]
		# ExportFbx(exported_objects, export_path = export_settings.export_path, export_name)

		# Restore scene.
		RestoreSceneObjectsFromCollected(exported_objects)

		self.report({'INFO'}, "Export finished.")
		return {'FINISHED'}

# -----------------------------------------------------------------------------------------
# 
# -----------------------------------------------------------------------------------------
class ExportHelper_OT_ExportByHelperName(Operator):
	"Description 1 " \
	"Description 2"
	bl_idname = "scene.eh_export_by_helpername"
	bl_label = "Export by helper name"

	def execute(self, context):
		export_settings =  bpy.context.scene.export_helper_settings

		if export_settings.use_debug is True:
			# Use debug infos.

			pass

		#randomSeed = export_settings.randomSeed if not self.defaultIvy else 0

		self.report({'INFO'}, "Export finished.")
		return {'FINISHED'}

# -----------------------------------------------------------------------------------------
# Export from root collection with all subcollections.
#
# Each collection exported as single fbx.
# Collection name must started with "_export_"
# -----------------------------------------------------------------------------------------
class ExportHelper_OT_ExportByCollection(Operator):
	"Description 1 " \
	"Description 2"
	bl_idname = "scene.eh_export_by_collection"
	bl_label = "Export"

	def execute(self, context):
		export_settings =  bpy.context.scene.export_helper_settings
		
		all_objects = context.scene.objects
		exported_objects = []

		print("-------------------------------------------------------")

		b_scene = BlenderScene(context.scene)
		b_scene.GetCollections()
		for c_obj in b_scene.collections:
			print("> ", c_obj.name, c_obj.is_select, c_obj.is_visible,	c_obj.is_render)


		self.report({'INFO'}, "Export finished.")
		return {'FINISHED'}
	
	# def execute(self, context):
	# 	export_settings =  bpy.context.scene.export_helper_settings
		
	# 	all_objects = context.scene.objects
	# 	exported_objects = []

	# 	if (export_settings.export_from_selected_collections):
	# 		# Export only from active and selected collection.

	# 		active_col_name = bpy.context.collection.name #bpy.context.view_layer.active_layer_collection.name
	# 		if (active_col_name.startswith('_export_')):
	# 			#exported_objects = GetExportedObjectsFromCollection(all_objects, ["Collection 2", "Collection 1"])
	# 			exported_objects = GetExportedObjectsFromCollection(all_objects, [active_col_name])
				
	# 			UnhideAndUnfreezeAll(exported_objects)

	# 			# Take file name from collection.
	# 			file_name = active_col_name[8:]

	# 			# Export.
	# 			ExportFbx([exported_objects], export_path = export_settings.export_path, export_name = file_name)

	# 			# Deselect all.

	# 	else:
	# 		# Export from all collections.

	# 		pass

	# 	for o in exported_objects:
	# 	 	print(o.obj.name)

	# 	# Restore scene.
	# 	RestoreScene([exported_objects])
	# 	#RestoreSceneObjectsFromCollected(exported_objects)

	# 	self.report({'INFO'}, "Export finished.")
	# 	return {'FINISHED'}

# -----------------------------------------------------------------------------------------
# Export from root collection with all subcollections.
#
# Each collection exported as single fbx.
# Collection name must started with "_export_"
# -----------------------------------------------------------------------------------------
class ExportHelper_OT_ExportByCollectionSeparateFiles(Operator):
	"Description 1 " \
	"Description 2"
	bl_idname = "scene.eh_export_by_collection_separate_files"
	bl_label = "Export sepatrate"

	def execute(self, context):
		export_settings =  bpy.context.scene.export_helper_settings
		
		all_objects = context.scene.objects
		exported_objects = []

		print("-------------------------------------------------------")

		active_col_name = bpy.context.collection.name
		exported_objects = GetExportedObjectsFromCollection(all_objects, [active_col_name])
		for b_obj in exported_objects:
			print("> ", b_obj.obj.name, b_obj.is_select, b_obj.is_visible,	b_obj.is_render)
			# ExportFbx(exported_objects, export_path = export_settings.export_path, export_name)

			bpy.ops.object.select_all(action='DESELECT')
			b_obj.obj.select_set(True)

			path = export_settings.export_path + b_obj.obj.name + ".fbx"
			bpy.ops.export_scene.fbx(filepath = path, **unity_kwargs)


		self.report({'INFO'}, "Export finished.")
		return {'FINISHED'}

# -----------------------------------------------------------------------------------------
# Export from root collection with all subcollections.
#
# 
# 
# -----------------------------------------------------------------------------------------
class ExportHelper_OT_ExportByCollectionGroupedFiles(Operator):
	"Description 1 " \
	"Description 2"
	bl_idname = "scene.eh_export_by_collection_grouped_files"
	bl_label = "Export grouped in each file"

	def execute(self, context):
		export_settings =  bpy.context.scene.export_helper_settings
		
		active_col_name = bpy.context.collection.name
		#all_objects = context.scene.objects
		all_objects = bpy.data.collections.get(active_col_name).all_objects

		exported_objects = []
		already_exported = []

		print("-------------------------------------------------------")

		
		# exported_objects = GetExportedObjectsFromCollection(all_objects, [active_col_name])
		child_colls = bpy.data.collections.get(active_col_name).children.keys()
		child_colls.append(active_col_name)
		exported_objects = GetExportedObjectsFromCollection(all_objects, child_colls)
		

		for b_obj in exported_objects:
			current_exported = []

			if (b_obj in already_exported):
				continue

			# print("> ", b_obj.obj.name, b_obj.is_select, b_obj.is_visible,	b_obj.is_render)

			# get object for export (must ending _LOD).
			#indx = b_obj.obj.name.index("_LOD")
			indx = b_obj.obj.name.find("_LOD")
			# print("------- ", b_obj.obj.name, ", ", indx)
			if (indx == -1):
		  		# Not found '_LOD'
				already_exported.append(b_obj)
				continue

			# get all grouped (lods, outline, shadows).
			base_name = b_obj.obj.name[0:indx]
			# print("Base name: ", base_name)
			for s_obj in exported_objects:
				if (s_obj in already_exported):
					continue

				# indx = s_obj.obj.name.startswith(base_name)
				# # # print(base_name, " ", indx)
				# if (not indx):
		  		# 	continue
				s_indx = s_obj.obj.name.find("_LOD")
				if (b_obj.obj.name[0:indx] == s_obj.obj.name[0:s_indx]):
					# print(b_obj.obj.name[0:indx], " -- ", s_obj.obj.name[0:indx])
					current_exported.append(s_obj)


			# export.
			bpy.ops.object.select_all(action='DESELECT')
			for e_obj in current_exported:
				e_obj.obj.select_set(True)
				#print("> ", e_obj.obj.name, e_obj.is_select, e_obj.is_visible,	e_obj.is_render)

			if (len(current_exported) > 0):
				path = export_settings.export_path + base_name + ".fbx"
				bpy.ops.export_scene.fbx(filepath = path, **unity_kwargs)

				# add objects to exported.
				for e_obj in current_exported:
					already_exported.append(e_obj)


		self.report({'INFO'}, "Export finished.")
		return {'FINISHED'}

# -----------------------------------------------------------------------------------------
# 
# -----------------------------------------------------------------------------------------
class ExportHelper_OT_AddRemove_NOEXP(Operator):
	"Description"
	bl_idname = "scene.eh_add_remove_noexp"
	bl_label = "Add or remove __NOEXP__ suffix to collection."

	def execute(self, context):
		active_col = bpy.context.collection.name
		if (active_col[0:9] == '__NOEXP__'):
			# Remove
			bpy.context.collection.name = active_col[9:]
		else:
			# Add
			bpy.context.collection.name = '__NOEXP__' + active_col
		
		return {'FINISHED'}

# -----------------------------------------------------------------------------------------
# 
# -----------------------------------------------------------------------------------------
class ExportHelper_OT_DeleteOutlineAndRecreate(Operator):
	"Description 1 " \
	"Description 2"
	bl_idname = "scene.eh_delete_outline_and_recreate"
	bl_label = "Delete outline and create new from active layer."

	def execute(self, context):
		if (bpy.context.mode != 'OBJECT'):
			bpy.ops.object.mode_set(mode='OBJECT')
		
		active_col_name = bpy.context.collection.name

		# delete outlines
		all_objects = bpy.data.collections.get(active_col_name).objects
		for o in all_objects:
			if (o.name.find("_outline") != -1):
				bpy.data.objects.remove(o, do_unlink = True)
		
		# recreate
		created_objs = []
		all_objects = bpy.data.collections.get(active_col_name).objects
		for o in all_objects:
			copy_obj = o.copy()
			copy_obj.data = o.data.copy()
			copy_obj.name = o.name + "_outline"
			created_objs.append(copy_obj)
		
		for o in created_objs:
			bpy.context.collection.objects.link(o)
			
		# clean
		for o in created_objs:
			#ApplyTransform(o)
			Delete_all_uvs(o)
			Delete_all_vcols(o)
			Delete_all_materials(o)
			Set_all_smooth(o)
		

		self.report({'INFO'}, "Clean outline and shadow meshes finished.")
		return {'FINISHED'}

# -----------------------------------------------------------------------------------------
# 
# -----------------------------------------------------------------------------------------
class ExportHelper_OT_CleanSelectedMeshes(Operator):
	"Description 1 " \
	"Description 2"
	bl_idname = "scene.eh_clean_selected_meshes"
	bl_label = "Clean meshes for outline and shadow"

	def execute(self, context):
		# turn off undo
		#undo = bpy.context.user_preferences.edit.use_global_undo
		#bpy.context.user_preferences.edit.use_global_undo = False

		if (bpy.context.mode != 'OBJECT'):
			bpy.ops.object.mode_set(mode='OBJECT')

		selected_objs = bpy.context.selected_objects
		for obj in selected_objs:
			# Clean mesh.
			#ApplyTransform(obj)
			Delete_all_uvs(obj)
			Delete_all_vcols(obj)
			Delete_all_materials(obj)
			Set_all_smooth(obj)

			#bpy.ops.mesh.customdata_custom_splitnormals_clear()

		self.report({'INFO'}, "Clean meshes finished.")
		return {'FINISHED'}

# -----------------------------------------------------------------------------------------
# 
# -----------------------------------------------------------------------------------------
class ExportHelper_OT_CleanSmoothData(Operator):
	"Description 1 " \
	"Description 2"
	bl_idname = "scene.eh_clean_smooth_data"
	bl_label = "Clean meshes for outline and shadow"

	def execute(self, context):
		# turn off undo
		#undo = bpy.context.user_preferences.edit.use_global_undo
		#bpy.context.user_preferences.edit.use_global_undo = False

		if (bpy.context.mode != 'OBJECT'):
			bpy.ops.object.mode_set(mode='OBJECT')

		selected_objs = bpy.context.selected_objects
		for obj in selected_objs:
			Set_all_smooth(obj)
			#bpy.ops.mesh.customdata_custom_splitnormals_clear()

		self.report({'INFO'}, "Clean meshes finished.")
		return {'FINISHED'}

# -----------------------------------------------------------------------------------------
# 
# -----------------------------------------------------------------------------------------
class ExportHelper_OT_ShowHideOutlines(Operator):
	"Description 1 " \
	"Description 2"
	bl_idname = "scene.eh_showhide_outlines"
	bl_label = "Show/hide outlones in active layer."

	hide: BoolProperty(default = True, options={'HIDDEN'})

	def execute(self, context):
		if (bpy.context.mode != 'OBJECT'):
			bpy.ops.object.mode_set(mode='OBJECT')
		
		active_col_name = bpy.context.collection.name

		# delete outlines
		all_objects = bpy.data.collections.get(active_col_name).all_objects
		for o in all_objects:
			if (o.name.find("_outline") != -1):
				o.hide_set(self.hide)
		

		self.report({'INFO'}, "Finished.")
		return {'FINISHED'}

# -----------------------------------------------------------------------------------------
# UV billboard.
# -----------------------------------------------------------------------------------------
class ExportHelper_OT_UVBillboardCreate(Operator):
	"Description 1 " \
	"Description 2"
	bl_idname = "scene.eh_uv_billboard_create"
	bl_label = "Create UV for billboard."

	def execute(self, context):
		if (bpy.context.mode != 'OBJECT'):
			bpy.ops.object.mode_set(mode='OBJECT')
		
		selected_objs = bpy.context.selected_objects
		for obj in selected_objs:
			if (obj.type != 'MESH'):
				continue

			# Check if uv exist.
			if (len(obj.data.uv_layers) < 1):
				print("Need diffuse uv first.")
				continue

			uvs = obj.data.uv_layers.keys()

			if (not 'UVBillboard1' in uvs):
				# print("Create UVBillboard1")
				obj.data.uv_layers.new(name='UVBillboard1', do_init = False)
			if (not 'UVBillboard2' in uvs):
				# print("Create UVBillboard1")
				obj.data.uv_layers.new(name='UVBillboard2', do_init = False)

			# write uvs.
			# obj.data.uv_layers.active = obj.data.uv_layers['UVBillboard1']
			# for loop in obj.data.loops:
			# 	obj_pos = obj.location
			# 	obj.data.uv_layers.active.data[loop.index].uv = Vector((obj_pos.x, obj_pos.y))
			# 	pass
			for loop in obj.data.loops:
				obj_pos = obj.location
				obj.data.uv_layers.active = obj.data.uv_layers['UVBillboard1']
				obj.data.uv_layers.active.data[loop.index].uv = Vector((obj_pos.x, obj_pos.y))
				obj.data.uv_layers.active = obj.data.uv_layers['UVBillboard2']
				obj.data.uv_layers.active.data[loop.index].uv = Vector((obj_pos.z, 0))
			
			# Restore active uv.
			obj.data.uv_layers.active = obj.data.uv_layers['UVMap']
			# obj.data.uv_layers["UVMap"].active_render = True

		self.report({'INFO'}, "Finished.")
		return {'FINISHED'}

class ExportHelper_OT_UVBillboardDelete(Operator):
	"Description 1 " \
	"Description 2"
	bl_idname = "scene.eh_uv_billboard_delete"
	bl_label = "Delete UV for billboard."

	def execute(self, context):
		if (bpy.context.mode != 'OBJECT'):
			bpy.ops.object.mode_set(mode='OBJECT')

		self.report({'INFO'}, "Finished.")
		return {'FINISHED'}


# -----------------------------------------------------------------------------------------
# Help.
# -----------------------------------------------------------------------------------------
class ExportHelper_OT_ExportHelp(Operator):
	bl_idname = "help.eh_export_help"
	bl_label = "Help"
	bl_description = "Tool Help - click to read some basic information"
	bl_options = {"REGISTER", "INTERNAL"}

	help_category: StringProperty(default="", options={'HIDDEN'})

	def draw(self, context):
		layout = self.layout
		
		if (self.help_category == "EXPORT_BY_NAME"):
			layout.label(text = "Export meshes by name:")
			layout.separator()
			layout.label(text = "")
			layout.label(text = "For example all objects")
			layout.label(text = "\tbig_stone_01_LOD0")
			layout.label(text = "\tbig_stone_01_LOD0_outline")
			layout.label(text = "\tbig_stone_01_LOD0_shadow")
			layout.label(text = "\tbig_stone_01_LOD1")
			layout.label(text = "\tbig_stone_01_LOD1_outline")
			layout.label(text = "\tbig_stone_01_LOD1_shadow")
			layout.label(text = "will be exported in big_stone_01.fbx")
		
		if (self.help_category == "EXPORT_BY_HELPERNAME"):
			layout.label(text = "Export meshes by helper name:")
			layout.separator()
			layout.label(text = "Scene must contain visible empty object with name started as '_export_'.")
			layout.label(text = "")
			layout.label(text = "For example visible objects with helper '_export_big_stone_01' will be exported as 'big_stone_01.fbx'.")
		
		if (self.help_category == "EXPORT_BY_COLLECTION"):
			layout.label(text = "Export meshes by collection:")
			layout.separator()
			layout.label(text = "Root collection with name started as '_export_'.")
			layout.label(text = "")

		if (self.help_category == "CLEAN_OUTLINE_AND_SHADOW"):
			layout.label(text = "Clean outline and shadow meshes:")
			layout.separator()
			layout.label(text = "Works on all objects in the scene.")
			layout.label(text = "Removes UV, vertex color, smooth group.")
		
		if (self.help_category == "REPOSITORY_HELP"):
			layout.label(text = "Blender file not in art repository.", icon='CANCEL')
			layout.label(text = "Art repository must contain")
			layout.label(text = "\'<ProjectName>\Models\' for models, with any number of subfolders within.")
			layout.label(text = "")
			layout.label(text = "For example <ProjectName>\Models\Trees\BigTrees\BigTree_01.blend")

	def execute(self, context):
		return {'FINISHED'}

	def invoke(self, context, event):
		return context.window_manager.invoke_popup(self, width=500)


# -----------------------------------------------------------------------------------------
# Register/Unregister.
# -----------------------------------------------------------------------------------------
classes = (
	ExportHelper_OT_ExportByName,
	ExportHelper_OT_ExportByHelperName,
	ExportHelper_OT_ExportByCollection,
	ExportHelper_OT_ExportByCollectionSeparateFiles,
	ExportHelper_OT_ExportByCollectionGroupedFiles,
	ExportHelper_OT_CleanSelectedMeshes,
	ExportHelper_OT_DeleteOutlineAndRecreate,
	ExportHelper_OT_CleanSmoothData,
	ExportHelper_OT_ShowHideOutlines,
	ExportHelper_OT_AddRemove_NOEXP,
	ExportHelper_OT_UVBillboardCreate,
	ExportHelper_OT_UVBillboardDelete,
	ExportHelper_OT_ExportHelp,
)

def register():
	from . import functions

	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)


def unregister():
	from bpy.utils import unregister_class
	for cls in classes:
		unregister_class(cls)
