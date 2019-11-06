## Imports Animated Alembic Geometry Cache into Unreal ##

import unreal as ue

## Locaiton of Alembic file on disk
assetLocation = 'Z:\Desktop\shaunTest2.abc'

## Makes folder in UE and sets asset path
assetPath = '/Game/Content/test'
ue.EditorAssetLibrary.make_directory(assetPath)

## Starts Asset Import
importTask = ue.AssetImportTask()
importTask.filename = 'Z:\Desktop\shaunTest2.abc'
importTask.destination_path = assetPath
importTask.destination_name = 'test'
importTask.automated = True

## Sets Alembic Import Options
importTask.options = ue.AbcImportSettings()
importTask.options.import_type = ue.AlembicImportType.GEOMETRY_CACHE
importTask.options.geometry_cache_settings = ue.AbcGeometryCacheSettings(flatten_tracks=False)
importTask.options.sampling_settings = ue.AbcSamplingSettings(frame_start=960, frame_end=1007, skip_empty=True)
importTask.options.normal_generation_settings = ue.AbcNormalGenerationSettings(recompute_normals=True)
importTask.options.material_settings = ue.AbcMaterialSettings(create_materials=True, find_materials=True)
importTask.options.conversion_settings = ue.AbcConversionSettings(rotation=[-90, 0, 0])

## Runs Final Import Command
imported_asset = ue.AssetToolsHelpers.get_asset_tools().import_asset_tasks([importTask])
