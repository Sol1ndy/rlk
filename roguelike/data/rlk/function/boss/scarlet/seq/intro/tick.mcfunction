# CS0 intro (PLAN §3.1): seated with the cup and bottle, lines 1-10, the walk, the scabbard raised; intro_end: line 11, the draw, the stance.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 640.
execute if score #sq hr matches 640.. run scoreboard players set #sqdone hr 1
execute if score #sq hr matches ..146 run return run function rlk:boss/scarlet/seq/intro/b/20_146
execute if score #sq hr matches ..254 run return run function rlk:boss/scarlet/seq/intro/b/198_254
execute if score #sq hr matches ..264 run return run function rlk:boss/scarlet/seq/intro/b/255_264
execute if score #sq hr matches ..344 run return run function rlk:boss/scarlet/seq/intro/b/265_344
execute if score #sq hr matches ..444 run return run function rlk:boss/scarlet/seq/intro/b/352_444
execute if score #sq hr matches ..606 run return run function rlk:boss/scarlet/seq/intro/b/452_606
execute if score #sq hr matches ..636 run return run function rlk:boss/scarlet/seq/intro/b/610_636
