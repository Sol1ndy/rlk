# CS0 intro (PLAN §3.1): seated with the cup and bottle, lines 1-10, the walk, the scabbard raised; intro_end: line 11, the draw, the stance.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 640.
execute if score #sq hr matches 640.. run scoreboard players set #sqdone hr 1
scoreboard players set @a[tag=player] hudHold 2
execute if score #sq hr matches ..118 run return run function rlk:boss/scarlet/seq/intro/b/20_118
execute if score #sq hr matches ..253 run return run function rlk:boss/scarlet/seq/intro/b/146_253
execute if score #sq hr matches ..263 run return run function rlk:boss/scarlet/seq/intro/b/254_263
execute if score #sq hr matches ..336 run return run function rlk:boss/scarlet/seq/intro/b/264_336
execute if score #sq hr matches ..410 run return run function rlk:boss/scarlet/seq/intro/b/344_410
execute if score #sq hr matches ..604 run return run function rlk:boss/scarlet/seq/intro/b/444_604
execute if score #sq hr matches ..636 run return run function rlk:boss/scarlet/seq/intro/b/606_636
