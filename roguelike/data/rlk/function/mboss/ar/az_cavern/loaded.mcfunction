# 1 when the box corners and the centre of az_cavern are loaded, else fail.
execute in minecraft:overworld unless loaded 280 201 -32 run return fail
execute in minecraft:overworld unless loaded 360 201 48 run return fail
execute in minecraft:overworld unless loaded 320 201 8 run return fail
return 1
