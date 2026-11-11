# CS1 (hr_design §3.2): the clash, pushed apart, the hat and the bottle, the petal, 홍련일섬, the crimson field; locked 0-720, skippable 40-560 -> 566.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 720.
execute if score #sq hr matches 720.. run scoreboard players set #sqdone hr 1
scoreboard players set @a[tag=player] hudHold 2
execute if score #sq hr matches ..719 unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/cs1/lock
function rlk:boss/scarlet/seq/cs1/skipin
execute if score #sq_skn hr matches 1 run return run scoreboard players set #sq_skn hr 0
execute if score #sq hr matches 6..32 run return run function rlk:boss/scarlet/seq/cs1/kb/6_32
execute if score #sq hr matches 34..238 run return run function rlk:boss/scarlet/seq/cs1/kb/34_238
execute if score #sq hr matches 240..592 run return run function rlk:boss/scarlet/seq/cs1/kb/240_592
execute if score #sq hr matches 593..607 run return run function rlk:boss/scarlet/seq/cs1/kb/593_607
execute if score #sq hr matches 608..622 run return run function rlk:boss/scarlet/seq/cs1/kb/608_622
execute if score #sq hr matches 623..637 run return run function rlk:boss/scarlet/seq/cs1/kb/623_637
execute if score #sq hr matches 638..652 run return run function rlk:boss/scarlet/seq/cs1/kb/638_652
execute if score #sq hr matches 653..720 run return run function rlk:boss/scarlet/seq/cs1/kb/653_720
