import bpy

# List of first mix of shapekeys
mayu_keys = [
    "name of your shape keys",
    "name of your shape keys",
    "name of your shape keys",
]

# List of second mix of shapekeys
eyebrow_keys = {
    "EyeBrow_22_R(Offset_D)[M_Mayu]": 0.2,
    "EyeBrow_22_L(Offset_D)[M_Mayu]": 0.2,
}

obj = bpy.context.object
if not obj or not obj.data.shape_keys:
    raise Exception("Select the mesh object with shapekeys before running this script")

kb = obj.data.shape_keys.key_blocks

for mayu in mayu_keys:
    if mayu not in kb:
        print(f"Skipping missing shapekey: {mayu}")
        continue

    # Reset all values
    for sk in kb:
        sk.value = 0.0

    # Activate
    kb[mayu].value = 1.0

    # Add eyebrows
    for brow, val in eyebrow_keys.items():
        if brow in kb:
            kb[brow].value = val

    # Create new shapekey from current mix
    new_key = obj.shape_key_add(from_mix=True)
    new_name = mayu.replace("_op_0", "_cl_0")     # name based on corresponding shape keys in this case cl for closed position and op for open for ussually for eyes and mouth
    new_key.name = new_name

    # Reset for safety
    for sk in kb:
        sk.value = 0.0

    # Move the new key just above the original
    bpy.context.object.active_shape_key_index = kb.find(new_name)
    target_index = kb.find(mayu)
    for _ in range(len(kb)):
        bpy.ops.object.shape_key_move(type='UP')
        if bpy.context.object.active_shape_key_index == target_index:
            break

print("✅ Done: All mayuge.*_cl_0 shapekeys created above their mayuge.*_op_0 counterparts")
 