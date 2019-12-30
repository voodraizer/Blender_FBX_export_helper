bl_info = {
	"name": "Fbx export helper",
	"description": "",
	"author": "",
	"version": (0,0,1),
	"blender": (2, 80, 0),
	"location": "File > Import/Export, Scene properties, Armature properties",
	"warning": 'work in progress',
	"wiki_url": "",
	"tracker_url": "",
	"category": "Import-Export"}

########################## TODO LIST ##########################################
# В экспортёре сделать вкладку проекты с путями к проектам (посмотреть пример в капсуле батч экспорт)
# 	кнопка экспорта одна с надписью экспорт, а в параметр оператора передавать тип экспорта
#
# Экспортить инстансинговые группы.
# Выводить лог в плавающую консоль с возмжностью её отключения.

#		!!! заносить специфические данные для данного файла в дамми экспорта
#		!!! сделать настройки рескейла, пивот в центр ...
#		Правильно передавать параметры в фбх экспортёр
#		делать триангуляцию объектов (добавлять модификатор триангулате, если его ещё нет)

#		!!! проверить экспорт
#			объекты на разных слоях и в разных состояниях, объекты с назначенной текстурой в юв окне ..., колижены
#			проверить в анриле модель экспорченную с экспортёром и без
#		как находить и устаналвивать путь до пресетов
#		+- исправить ошибку из консоли, когда юзеров -1
#		-- запоминать последний использованный путь (добавить AddPreset)
#				для параметров префсов юзать локальные переменные (а не в scene)
#				выдавать предупреждение при первом экспорте для установки пути к проекту и др.
#
#		!!! экспортить колижены (даже если они скрыты, но не с разрешённым рендером)
#		!!! экспортить набор анимаций с правильными параметрами
#		читать анимации (названия, длительность...) из dope sheet (или аналога)
#		делать еденичные матрицы трансформации (ресетить скейл и поворот)
#		убирать анимацию у статичных объектов
#		++- экспорт без анду (чтобы не менять сохранённой сцены)
#		+++ убрать спам в консоли не найден локальный путь, не найден путь к проекту
#		конвертить сплайны в меш для экспорта (если они не экспортятся так)
#		!!!посмотреть как экспортится порядок материалов в движок (от чего зависит и как фиксить)
#				зависит от порядка добавления объектов в сцену (раздел Connections:). надо фиксить сортируя Connect: по материалам (задавать порядок через _Mat01 ...)
#				порядок посмотреть можно bpy.context.scene.objects.keys(), bpy.context.scene.objects.values()
#				перед дублированием объектов(в массив темп обжектс) надо сортировать их по материалам
#		экспортить лоды
#		проверить надо ли мержить объекты по материалам по причине производительности
###############################################################################

#--------------------------------------------------------------------------------------------------
# RTFM
#--------------------------------------------------------------------------------------------------
# 1. задать путь к симметричному проекту (рабочий репозиторий) в файле 'settings\projects.py'
# 2. запустить блендер, включить аддон
# 3. задать на видимом слое DUMMY объект и назвать его _export_<имя_экспортируемого_файла> (напр. _export_TreeBig_01a)
#		объекты мержатся к объекту названному 'base'. следовательно порядок юв и вертекс-колор слоёв должен совпадать с базовым.
#		если базового объекта нет, то все объекты мержатся к персому объекту в сцене. Порядок юв и вертекс-колор слоёв в данном случае не гарантирован
# 4. структура папок арт репозитория .....
#
# 9. путь экспортированного файла будет: <путь к проекту>\<путь до файла в арт-репозитории>\_exported\<имя_экспортируемого_файла>.fbx
#				для симметричного пути: <симметричный путь>\<путь до файла в арт-репозитории>\<имя_экспортируемого_файла>.fbx
# 10. экспортятся все объекты на видимых слоях (за исключением _export_<имя_экспортируемого_файла> и особо оговорённых случаев)
# 11. объекты с выключенным рендером (значок фотоаппарата в аутлайнере) не будут проэкспортированы
# 
#--------------------------------------------------------------------------------------------------




import bpy
import os
import platform
from bpy.types import Menu, Panel, Operator
from bpy.props import BoolProperty, IntProperty, EnumProperty, StringProperty, PointerProperty, CollectionProperty


# Support 'reload' case.
if "bpy" in locals():
	import importlib
	if "functions" in locals():
		importlib.reload(functions)
	if "operators" in locals():
		importlib.reload(operators)




class Addon_UI(bpy.types.Panel):
	bl_idname = "Fbx export helper."
	bl_label = "Fbx export helper."
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "scene"
	
	
	
	def draw(self, context):
		scene = context.scene
		# fbx_helper = context.scene.fbx_helper_settings
		export_settings = bpy.context.scene.export_helper_settings
		
		layout = self.layout
		
		layout.separator()

		col = layout.column(align=True)
		row = col.split(factor=0.95)
		row.prop(export_settings, "export_type")
		row.operator("help.eh_export_help", text="", icon="QUESTION").help_category = export_settings.export_type

		# -----------------------------------------------------------------------------------------
		# Export buttons.
		# -----------------------------------------------------------------------------------------
		if (os.path.exists(export_settings.export_path)):
			if (export_settings.export_type == 'EXPORT_BY_NAME'):
				row = layout.row()
				op = row.operator("scene.eh_export_by_name", text="Export by name", icon='EXPORT')

			if (export_settings.export_type == 'EXPORT_BY_HELPERNAME'):
				row = layout.row()
				op = row.operator("scene.eh_export_by_helpername", text="Export by helper name", icon='EXPORT')
				#op.export_name = export_name
				#op.export_file = export_file
				#op.presetpath = os.path.join(os.path.dirname(__file__), 'settings')
			
			if (export_settings.export_type == 'EXPORT_BY_COLLECTION'):
				row = layout.row()
				op = row.operator("scene.eh_export_by_collection", text="Export", icon='EXPORT')
				row = layout.row()
				op = row.operator("scene.eh_export_by_collection_separate_files", text="Export separate", icon='EXPORT')
				row = layout.row()
				op = row.operator("scene.eh_export_by_collection_grouped_files", text="Export grouped in each file", icon='EXPORT')

		# -----------------------------------------------------------------------------------------
		# Export path.
		# -----------------------------------------------------------------------------------------
		layout.separator()
		layout.separator()

		row = layout.row()
		row.label(text = "Export path:")
		row = layout.row()
		
		if (not os.path.exists(export_settings.export_path)):
			# Path not set correctly.
			#row.enabled = False
			row.alert = True
			row.prop(export_settings, 'export_path', text="")
			row = layout.row()
			#row.enabled = True
			box = row.box()
			colsub = box.column()
			r = colsub.row()
			r.label(text="Path not found.", icon='CANCEL')
		else:
			row.prop(export_settings, 'export_path', text="")

		layout.separator()

		if (not export_settings.display_geometry):
			layout.row().prop(export_settings, 'display_geometry', icon = 'RIGHTARROW', text = 'Geometry')
		else:
			layout.row().prop(export_settings, 'display_geometry', icon = 'DOWNARROW_HLT', text = 'Geometry')
			box = layout.column(align=True).box().column()
			#box.separator()

			box_i = box.box()
			box_i.prop(export_settings, "merge_all_geometry", text = "Merge geometry")

			box_i = box.box()
			box_i.label(text = "Skip export objects by:")

			split = box_i.split()
			col = split.row(align = True)
			col.prop(export_settings, "export_freeze", text = "Freeze")
			col.prop(export_settings, "export_hidden", text = "Hidden")
			col.prop(export_settings, "export_renderable", text = "Renderable")

			box_i.separator()
			box_i.prop(export_settings, "export_from_selected_collections", text = "Export from selected collection")
			

		# -----------------------------------------------------------------------------------------
		# Debug utils.
		# -----------------------------------------------------------------------------------------
		if (not export_settings.use_utils):
			layout.row().prop(export_settings, 'use_utils', icon = 'RIGHTARROW', text = 'Utils')
		else:
			layout.row().prop(export_settings, 'use_utils', icon = 'DOWNARROW_HLT', text = 'Utils')
			
			layout.separator()
			#layout.alignment = 'CENTER'
			#row.alignment = 'CENTER'
			layout.label(text = "----- Rename -----")
			row = layout.split(factor=0.95)
			row.operator('scene.eh_add_remove_noexp', text = 'Collection add/remove __NOEXP__')
			row.operator("help.eh_export_help", text="", icon="QUESTION").help_category = ""

			layout.separator()
			layout.label(text = "----- Outline and Shadow meshes -----")
			
			row = layout.split(factor=0.95)
			row_i = row.split(factor=0.5)
			row_i.operator('scene.eh_clean_selected_meshes', text = 'Clean selected meshes')
			row_i.operator('scene.eh_clean_smooth_data', text = 'Clean smooth data')
			row.operator("help.eh_export_help", text="", icon="QUESTION").help_category = ""

			row = layout.split(factor=0.95)
			row_i = row.split(factor=0.5)
			row_i.operator('scene.eh_showhide_outlines', text = 'Show outlines').hide = False
			row_i.operator('scene.eh_showhide_outlines', text = 'Hide outlines').hide = True
			row.operator("help.eh_export_help", text="", icon="QUESTION").help_category = ""

			row = layout.split(factor=0.95)
			row.operator('scene.eh_delete_outline_and_recreate', text = 'Delete outlines and recreate')
			row.operator("help.eh_export_help", text="", icon="QUESTION").help_category = ""
			
			layout.separator()
			layout.label(text = "----- UV billboard -----")
			
			row = layout.split(factor=0.95)
			row_i = row.split(factor=0.5)

			row_i.operator('scene.eh_uv_billboard_create', text = 'Create billboard uv')
			row_i.operator('scene.eh_uv_billboard_delete', text = 'Delete billboard uv')
			row.operator("help.eh_export_help", text="", icon="QUESTION").help_category = ""



			#layout.row().operator('scene.uvs_rearrange', text = 'Rearrange UVs')

		# -----------------------------------------------------------------------------------------
		# 
		# -----------------------------------------------------------------------------------------


		pass


# -----------------------------------------------------------------------------------------
# Export helper settings.
# -----------------------------------------------------------------------------------------
class ExportHelperSettings(bpy.types.PropertyGroup):
	export_type: EnumProperty(
			name="ExportType",
			items=(
				('EXPORT_BY_NAME', "Export by name", ""),
				('EXPORT_BY_HELPERNAME', "Export by helper name", ""),
				('EXPORT_BY_COLLECTION', "Export by collection", ""),
				),
			description="",
			default='EXPORT_BY_HELPERNAME',
			#update=update_object,
			)

	export_path: StringProperty(
		name='Output directory path',
		description='',
		default='',
		subtype='DIR_PATH')
	
	display_geometry: BoolProperty(
		name="UseGeometry",
		description="",
		default=True)
	
	merge_all_geometry: BoolProperty(
		name="MergeAllGeometry",
		description="",
		default=False)
	
	export_freeze: BoolProperty(
		name="ExportFreeze",
		description="",
		default=True)
	
	export_hidden: BoolProperty(
		name="ExportHidden",
		description="",
		default=False)
	
	export_renderable: BoolProperty(
		name="ExportRenderable",
		description="",
		default=True)
	
	export_from_hidden_collections: BoolProperty(
		name="ExportFromHiddenCollections",
		description="",
		default=False)
	
	export_from_selected_collections: BoolProperty(
		name="ExportFromActiveAndSelectedCollections",
		description="",
		default=True)
	
	use_utils: BoolProperty(
		name="UseUtils",
		description="",
		default=False)

	use_debug: BoolProperty(
		name="UseDebug",
		description="",
		default=False)

	

# -----------------------------------------------------------------------------------------
# Register/Unregister.
# -----------------------------------------------------------------------------------------
classes = (
	Addon_UI,
	ExportHelperSettings,
)

def register():
	from bpy.utils import register_class

	from . import functions
	from . import operators
	
	operators.register()
	#export_objects.register()
	
	for cls in classes:
		register_class(cls)
	
	# get preset path
	#presetpath = os.path.join(os.path.dirname(__file__), 'settings')
	
	# load last settings
	#functions.LoadLastSettings()

	bpy.types.Scene.export_helper_settings = PointerProperty(type=ExportHelperSettings)

	

def unregister():
	from bpy.utils import unregister_class

	from . import functions
	from . import operators
		
	operators.unregister()
	#export_objects.unregister()
	
	for cls in classes:
		unregister_class(cls)
	
	try:
		del bpy.types.Scene.export_helper_settings
	except:
		pass

	
	

if __name__ == "__main__":
	register()

	