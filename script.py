import bpy

obj = bpy.context.object

if obj and obj.type == 'MESH':
    # Ensure vertex groups exist
    vg_base = obj.vertex_groups.get("cf_J_FaceBase") or obj.vertex_groups.new(name="cf_J_FaceBase")
    vg_root = obj.vertex_groups.get("cf_J_FaceRoot") or obj.vertex_groups.new(name="cf_J_FaceRoot")
    
    mesh = obj.data
    bpy.ops.object.mode_set(mode='OBJECT')

    # Collect selected vertex indices (hidden verts are still tracked)
    selected = [v.index for v in mesh.vertices if v.select]
    all_verts = [v.index for v in mesh.vertices]

    # Reset both groups to 0 for all verts
    for vid in all_verts:
        vg_base.add([vid], 0.0, 'REPLACE')
        vg_root.add([vid], 0.0, 'REPLACE')

    # Assign values based on selection
    for vid in all_verts:
        if vid in selected:
            vg_base.add([vid], 0.0, 'REPLACE')  # selected → 0 in FaceBase
            vg_root.add([vid], 1.0, 'REPLACE')  # selected → 1 in FaceRoot
        else:
            vg_base.add([vid], 1.0, 'REPLACE')  # others → 1 in FaceBase
            vg_root.add([vid], 0.0, 'REPLACE')  # others → 0 in FaceRoot

    bpy.ops.object.mode_set(mode='EDIT')
    print("Weights updated successfully.")
else:
    print("Select a mesh object in Object or Edit Mode.")
