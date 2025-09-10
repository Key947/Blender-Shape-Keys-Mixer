import bpy

# List of Mayu shapekeys (_op ones already exist)
mayu_keys = [
    "mayuge.mayu00_def_op",
    "mayuge.mayu01_angry_op",
    "mayuge.mayu02_worried_op",
    "mayuge.mayu03_bored_op",
    "mayuge.mayu04_doubtL_op",
    "mayuge.mayu05_doubtR_op",
    "mayuge.mayu06_thinkingL_op",
    "mayuge.mayu07_thinkingR_op",
    "mayuge.mayu08_angry2L_op",
    "mayuge.mayu09_angry2R_op",
    "mayuge.mayu10_serious_op",
    "mayuge.mayu11_anxious_op",
    "mayuge.mayu12_surprised_op",
    "mayuge.mayu13_disapointed_op",
    "mayuge.mayu14_smug_op",
    "mayuge.mayu15_winkL_op",
    "mayuge.mayu16_winkR_op",
]

# Eyebrow shapekeys that should always be added to the mix
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

    # Activate base mayu
    kb[mayu].value = 1.0

    # Add eyebrows
    for brow, val in eyebrow_keys.items():
        if brow in kb:
            kb[brow].value = val

    # Create new shapekey from current mix
    new_key = obj.shape_key_add(from_mix=True)
    new_name = mayu.replace("_op", "_cl")
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

print("✅ Done: All mayuge.*_cl shapekeys created above their mayuge.*_op counterparts")
