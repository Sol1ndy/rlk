# CS0 intro (hr_design §3.1): 20 shots, lines 1-11; seated with the cup and the bottle, the walk, the leap; intro_end: line 11, the draw, the stance.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 1440.
execute if score #sq hr matches 1440.. run scoreboard players set #sqdone hr 1
scoreboard players set @a[tag=player] hudHold 2
execute if score #sq hr matches ..1439 unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/intro/lock
function rlk:boss/scarlet/seq/intro/skipin
execute if score #sq_skn hr matches 1 run return run scoreboard players set #sq_skn hr 0
execute if score #sq hr matches 24..138 run return run function rlk:boss/scarlet/seq/intro/kb/24_138
execute if score #sq hr matches 139..165 run return run function rlk:boss/scarlet/seq/intro/kb/139_165
execute if score #sq hr matches 166..213 run return run function rlk:boss/scarlet/seq/intro/kb/166_213
execute if score #sq hr matches 214..474 run return run function rlk:boss/scarlet/seq/intro/kb/214_474
execute if score #sq hr matches 486..760 run return run function rlk:boss/scarlet/seq/intro/kb/486_760
execute if score #sq hr matches 762..982 run return run function rlk:boss/scarlet/seq/intro/kb/762_982
execute if score #sq hr matches 984..1148 run return run function rlk:boss/scarlet/seq/intro/kb/984_1148
execute if score #sq hr matches 1150..1440 run return run function rlk:boss/scarlet/seq/intro/kb/1150_1440
