# 1 when every chunk of the box of cp_test is loaded (the centre first), else fail.
execute in minecraft:overworld unless loaded 540 201 8 run return fail
execute in minecraft:overworld unless loaded 524 201 -8 run return fail
execute in minecraft:overworld unless loaded 524 201 0 run return fail
execute in minecraft:overworld unless loaded 524 201 16 run return fail
execute in minecraft:overworld unless loaded 528 201 -8 run return fail
execute in minecraft:overworld unless loaded 528 201 16 run return fail
execute in minecraft:overworld unless loaded 544 201 -8 run return fail
execute in minecraft:overworld unless loaded 544 201 0 run return fail
execute in minecraft:overworld unless loaded 544 201 16 run return fail
return 1
