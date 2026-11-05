# CS0 intro (PLAN §3.1): seated with the cup and bottle, lines 1-10, the walk, the scabbard raised; intro_end: line 11, the draw, the stance.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 640.
execute if score #sq hr matches 640.. run scoreboard players set #sqdone hr 1
execute if score #sq hr matches ..255 run return run function rlk:boss/scarlet/seq/intro/b/214_255
execute if score #sq hr matches ..265 run return run function rlk:boss/scarlet/seq/intro/b/256_265
execute if score #sq hr matches ..360 run return run function rlk:boss/scarlet/seq/intro/b/266_360
execute if score #sq hr matches ..484 run return run function rlk:boss/scarlet/seq/intro/b/368_484
execute if score #sq hr matches ..636 run return run function rlk:boss/scarlet/seq/intro/b/554_636
