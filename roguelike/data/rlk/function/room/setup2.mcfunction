# 청크가 아직 안 불러와졌으면 잠시 뒤 다시
execute in minecraft:overworld unless loaded -64 200 -64 run return run schedule function rlk:room/setup2 20t
execute in minecraft:overworld unless loaded 63 200 63 run return run schedule function rlk:room/setup2 20t
execute in minecraft:overworld run function rlk:room/wipe
execute as @a[tag=rlk_setup,limit=1] in minecraft:overworld run function rlk:room/setup3
