# CS0 intro (PLAN §3.1): seated with the cup and bottle, lines 1-10, the walk, the scabbard raised; intro_end: line 11, the draw, the stance.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 640.
execute if score #sq hr matches 640.. run scoreboard players set #sqdone hr 1
scoreboard players set @a[tag=player] hudHold 2
execute if score #sq hr matches ..118 run return run function rlk:boss/scarlet/seq/intro/b/20_118
execute if score #sq hr matches ..251 run return run function rlk:boss/scarlet/seq/intro/b/146_251
execute if score #sq hr matches ..261 run return run function rlk:boss/scarlet/seq/intro/b/252_261
execute if score #sq hr matches ..320 run return run function rlk:boss/scarlet/seq/intro/b/262_320
execute if score #sq hr matches ..398 run return run function rlk:boss/scarlet/seq/intro/b/328_398
execute if score #sq hr matches ..510 run return run function rlk:boss/scarlet/seq/intro/b/402_510
execute if score #sq hr matches ..636 run return run function rlk:boss/scarlet/seq/intro/b/554_636
