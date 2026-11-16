# repel {at:60|5} (hr_design §3.4): the deflect, the blade lock, the grab, the hilt on her hat, two cuts, back to back, the throw, the kick; HP steps at 49 / 101 / 129; locked 0-140, the bars on.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 140.
execute if score #sq hr matches 140.. run scoreboard players set #sqdone hr 1
scoreboard players set @a[tag=player] hudHold 2
execute if score #sq hr matches ..139 unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/repel/lock
execute if score #sq hr matches 4..8 run return run function rlk:boss/scarlet/seq/repel/kb/4_8
execute if score #sq hr matches 10..16 run return run function rlk:boss/scarlet/seq/repel/kb/10_16
execute if score #sq hr matches 19..25 run return run function rlk:boss/scarlet/seq/repel/kb/19_25
execute if score #sq hr matches 30..49 run return run function rlk:boss/scarlet/seq/repel/kb/30_49
execute if score #sq hr matches 56..68 run return run function rlk:boss/scarlet/seq/repel/kb/56_68
execute if score #sq hr matches 78..110 run return run function rlk:boss/scarlet/seq/repel/kb/78_110
execute if score #sq hr matches 129..139 run return run function rlk:boss/scarlet/seq/repel/kb/129_139
execute if score #sq hr matches 140 run return run function rlk:boss/scarlet/seq/repel/k/140
