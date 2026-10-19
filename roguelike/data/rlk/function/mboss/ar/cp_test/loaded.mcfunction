# 1 when the box corners and the centre of cp_test are loaded, else fail.
execute in minecraft:overworld unless loaded 524 201 -8 run return fail
execute in minecraft:overworld unless loaded 556 201 24 run return fail
execute in minecraft:overworld unless loaded 540 201 8 run return fail
return 1
