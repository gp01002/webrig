import bpy
import sys

# 清理場景
bpy.ops.wm.read_factory_settings(use_empty=True)

# 取得參數 (命令列傳入)
argv = sys.argv
try:
    argv = argv[argv.index("--") + 1:] 
    input_path = argv[0]
    output_path = argv[1]
except:
    print("Error: 請提供輸入和輸出路徑")
    sys.exit(1)

print(f"Blender: 正在處理 {input_path}")

try:
    # 1. 匯入 GLB/GLTF
    bpy.ops.import_scene.gltf(filepath=input_path)
    
    # 2. 找到主要網格物件
    mesh_obj = None
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            mesh_obj = obj
            break
            
    if mesh_obj:
        print(f"Blender: 找到網格 {mesh_obj.name}")
        
        # 3. 建立簡單骨架 (範例：單一骨骼)
        # 實務上這裡可以替換成更複雜的 Rigify 腳本
        bpy.ops.object.armature_add(enter_editmode=False, location=(0, 0, 0))
        armature = bpy.context.object
        armature.name = "AutoRig_Armature"
        
        # 根據模型高度調整骨架大小
        dim = mesh_obj.dimensions
        armature.scale = (dim.z/2, dim.z/2, dim.z/2)
        
        # 4. 綁定 (Automatic Weights)
        bpy.ops.object.select_all(action='DESELECT')
        mesh_obj.select_set(True)
        armature.select_set(True)
        bpy.context.view_layer.objects.active = armature
        
        # 執行自動權重
        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        print("Blender: 自動權重綁定完成")
        
    # 5. 匯出
    bpy.ops.export_scene.gltf(filepath=output_path)
    print("Blender: 匯出成功")

except Exception as e:
    print(f"Blender Error: {e}")
    sys.exit(1)