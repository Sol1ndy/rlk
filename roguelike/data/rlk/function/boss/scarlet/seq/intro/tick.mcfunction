# CS0 intro (hr_design §3.1): 20 shots, lines 1-11; seated with the cup and the bottle, the walk, the leap; intro_end: line 11, the draw, the stance.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 1440.
execute if score #sq hr matches 1440.. run scoreboard players set #sqdone hr 1
scoreboard players set @a[tag=player] hudHold 2
execute if score #sq hr matches ..1439 unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/intro/lock
execute if score #sq hr matches 20..153 run return run function rlk:boss/scarlet/seq/intro/kb/20_153
execute if score #sq hr matches 154..165 run return run function rlk:boss/scarlet/seq/intro/kb/154_165
execute if score #sq hr matches 166..182 run return run function rlk:boss/scarlet/seq/intro/kb/166_182
execute if score #sq hr matches 183..210 run return run function rlk:boss/scarlet/seq/intro/kb/183_210
execute if score #sq hr matches 211..462 run return run function rlk:boss/scarlet/seq/intro/kb/211_462
execute if score #sq hr matches 474..880 run return run function rlk:boss/scarlet/seq/intro/kb/474_880
execute if score #sq hr matches 906..1124 run return run function rlk:boss/scarlet/seq/intro/kb/906_1124
execute if score #sq hr matches 1136..1440 run return run function rlk:boss/scarlet/seq/intro/kb/1136_1440
