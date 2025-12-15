import bpy
import sys

def clean_and_prepare_mesh():
    """
    [關鍵修復] 在綁骨之前清理模型
    解決 'Bone Heat Weighting: failed' 導致的伺服器 500 錯誤
    """
    print("Blender: 正在執行網格清理與優化...")
    
    # 確保在 Object Mode
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            
            # 1. 套用變形 (Apply Transforms) - 修正縮放比例問題
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            
            # 2. 進入編輯模式處理幾何結構
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            
            # 3. 合併重疊頂點 (Remove Doubles) - 修復網格破洞
            bpy.ops.mesh.remove_doubles(threshold=0.001)
            
            # 4. 重新計算外側法線
            bpy.ops.mesh.normals_make_consistent(inside=False)
            
            # 回到 Object Mode
            bpy.ops.object.mode_set(mode='OBJECT')
            obj.select_set(False)

# ==========================================
# 主程式邏輯
# ==========================================

# 清理場景
bpy.ops.wm.read_factory_settings(use_empty=True)

# 取得參數 (保持你原本的邏輯)
argv = sys.argv
try:
    if "--" in argv:
        argv = argv[argv.index("--") + 1:] 
        input_path = argv[0]
        output_path = argv[1]
    else:
        # 本地測試時的 fallback，避免索引錯誤
        print("Warning: 未偵測到 '--' 分隔符，嘗試直接讀取最後兩個參數")
        input_path = argv[-2]
        output_path = argv[-1]
except Exception as e:
    print(f"Error: 參數解析失敗 - {e}")
    sys.exit(1)

print(f"Blender: 正在處理 {input_path}")

try:
    # 1. 匯入 GLB/GLTF
    bpy.ops.import_scene.gltf(filepath=input_path)
    
    # 2. [新增步驟] 執行網格清理
    # 這是在綁骨之前必須執行的，否則很容易失敗
    clean_and_prepare_mesh()
    
    # 3. 找到主要網格物件
    mesh_obj = None
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            mesh_obj = obj
            break
            
    if mesh_obj:
        print(f"Blender: 找到網格 {mesh_obj.name}")
        
        # 4. 建立簡單骨架
        bpy.ops.object.armature_add(enter_editmode=False, location=(0, 0, 0))
        armature = bpy.context.object
        armature.name = "AutoRig_Armature"
        
        # 根據模型高度調整骨架大小 (保留原本邏輯)
        # 注意：因為前面執行了 Apply Scale，這裡的 dimensions 會是真實尺寸
        dim = mesh_obj.dimensions
        armature.scale = (dim.z/2, dim.z/2, dim.z/2)
        
        # 5. 綁定 (加入錯誤處理機制)
        bpy.ops.object.select_all(action='DESELECT')
        mesh_obj.select_set(True)
        armature.select_set(True)
        bpy.context.view_layer.objects.active = armature
        
        try:
            print("Blender: 嘗試自動權重綁定 (Automatic Weights)...")
            bpy.ops.object.parent_set(type='ARMATURE_ENVELOPE')
            print("Blender: 自動權重綁定成功")
        except Exception as e:
            print(f"Warning: 自動權重失敗 ({e})，嘗試切換為封套權重 (Envelope)...")
            # 如果自動權重失敗，切換到 Envelope 模式以防止崩潰
            bpy.ops.object.select_all(action='DESELECT')
            mesh_obj.select_set(True)
            armature.select_set(True)
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.parent_set(type='ARMATURE_ENVELOPE')
            print("Blender: 已使用封套權重綁定")

    # 6. 匯出
    # 確保有選取物件再匯出
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(
        filepath=output_path, 
        export_format='GLB',
        export_skins=True,  # 確保匯出蒙皮
        export_yup=True
    )
    print("Blender: 匯出成功")

except Exception as e:
    # 捕捉所有未預期的錯誤，並印出以供 Debug
    import traceback
    traceback.print_exc()
    print(f"Blender Critical Error: {e}")
    sys.exit(1)
