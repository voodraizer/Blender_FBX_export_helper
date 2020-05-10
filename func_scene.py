import bpy

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