import bpy

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
# Get collection of objects.
#
#-----------------------------------------------------------------------------------------------------------------------------
def GetAllCollection(scene):
	scene_collections = []
	
	return scene_collections