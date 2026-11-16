# 1 when the centre of the plaza is loaded (the M0 test of mboss/start), else fail.
execute in minecraft:overworld unless loaded 200 201 8 run return fail
return 1
