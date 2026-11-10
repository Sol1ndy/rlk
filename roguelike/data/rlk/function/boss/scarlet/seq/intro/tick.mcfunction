# CS0 intro (hr_design §3.1): 20 shots, lines 1-11; seated with the cup and the bottle, the walk, the leap; intro_end: line 11, the draw, the stance.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 1440.
execute if score #sq hr matches 1440.. run scoreboard players set #sqdone hr 1
scoreboard players set @a[tag=player] hudHold 2
execute if score #sq hr matches ..1439 unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/intro/lock
execute if score #sq hr matches 24..151 run return run function rlk:boss/scarlet/seq/intro/kb/24_151
execute if score #sq hr matches 152..165 run return run function rlk:boss/scarlet/seq/intro/kb/152_165
execute if score #sq hr matches 166..184 run return run function rlk:boss/scarlet/seq/intro/kb/166_184
execute if score #sq hr matches 185..214 run return run function rlk:boss/scarlet/seq/intro/kb/185_214
execute if score #sq hr matches 215..690 run return run function rlk:boss/scarlet/seq/intro/kb/215_690
execute if score #sq hr matches 712..1076 run return run function rlk:boss/scarlet/seq/intro/kb/712_1076
execute if score #sq hr matches 1088..1294 run return run function rlk:boss/scarlet/seq/intro/kb/1088_1294
execute if score #sq hr matches 1352..1440 run return run function rlk:boss/scarlet/seq/intro/kb/1352_1440
