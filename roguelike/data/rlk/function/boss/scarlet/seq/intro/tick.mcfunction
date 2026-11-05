# CS0 intro (PLAN §3.1): seated with the cup and bottle, lines 1-10, the walk, the scabbard raised; intro_end: line 11, the draw, the stance.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 640.
execute if score #sq hr matches 640.. run scoreboard players set #sqdone hr 1
execute if score #sq hr matches ..257 run return run function rlk:boss/scarlet/seq/intro/b/248_257
execute if score #sq hr matches ..267 run return run function rlk:boss/scarlet/seq/intro/b/258_267
execute if score #sq hr matches ..376 run return run function rlk:boss/scarlet/seq/intro/b/268_376
execute if score #sq hr matches ..604 run return run function rlk:boss/scarlet/seq/intro/b/384_604
execute if score #sq hr matches ..636 run return run function rlk:boss/scarlet/seq/intro/b/610_636
