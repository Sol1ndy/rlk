# 1 when the box corners and the centre of plaza are loaded, else fail.
execute in minecraft:overworld unless loaded 176 201 -16 run return fail
execute in minecraft:overworld unless loaded 223 201 31 run return fail
execute in minecraft:overworld unless loaded 200 201 8 run return fail
return 1
