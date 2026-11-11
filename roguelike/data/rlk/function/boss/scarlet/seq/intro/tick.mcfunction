# CS0 intro (hr_design §3.1): 20 shots, lines 1-11; seated with the cup and the bottle, the walk, the leap; intro_end: line 11, the draw, the stance.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 1440.
execute if score #sq hr matches 1440.. run scoreboard players set #sqdone hr 1
scoreboard players set @a[tag=player] hudHold 2
execute if score #sq hr matches ..1439 unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/intro/lock
function rlk:boss/scarlet/seq/intro/skipin
execute if score #sq_skn hr matches 1 run return run scoreboard players set #sq_skn hr 0
execute if score #sq hr matches 24..160 run return run function rlk:boss/scarlet/seq/intro/kb/24_160
execute if score #sq hr matches 161..188 run return run function rlk:boss/scarlet/seq/intro/kb/161_188
execute if score #sq hr matches 189..346 run return run function rlk:boss/scarlet/seq/intro/kb/189_346
execute if score #sq hr matches 348..612 run return run function rlk:boss/scarlet/seq/intro/kb/348_612
execute if score #sq hr matches 624..841 run return run function rlk:boss/scarlet/seq/intro/kb/624_841
execute if score #sq hr matches 842..990 run return run function rlk:boss/scarlet/seq/intro/kb/842_990
execute if score #sq hr matches 1024..1148 run return run function rlk:boss/scarlet/seq/intro/kb/1024_1148
execute if score #sq hr matches 1150..1440 run return run function rlk:boss/scarlet/seq/intro/kb/1150_1440
