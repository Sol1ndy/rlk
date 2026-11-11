# CS1 (hr_design §3.2): the clash, pushed apart, the hat and the bottle, the petal, 홍련일섬, the crimson field; locked 0-720, skippable 40-560 -> 566.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 720.
execute if score #sq hr matches 720.. run scoreboard players set #sqdone hr 1
scoreboard players set @a[tag=player] hudHold 2
execute if score #sq hr matches ..719 unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/cs1/lock
function rlk:boss/scarlet/seq/cs1/skipin
execute if score #sq_skn hr matches 1 run return run scoreboard players set #sq_skn hr 0
execute if score #sq hr matches 6..22 run return run function rlk:boss/scarlet/seq/cs1/kb/6_22
execute if score #sq hr matches 24..118 run return run function rlk:boss/scarlet/seq/cs1/kb/24_118
execute if score #sq hr matches 162..272 run return run function rlk:boss/scarlet/seq/cs1/kb/162_272
execute if score #sq hr matches 464..591 run return run function rlk:boss/scarlet/seq/cs1/kb/464_591
execute if score #sq hr matches 592..602 run return run function rlk:boss/scarlet/seq/cs1/kb/592_602
execute if score #sq hr matches 603..642 run return run function rlk:boss/scarlet/seq/cs1/kb/603_642
execute if score #sq hr matches 645..658 run return run function rlk:boss/scarlet/seq/cs1/kb/645_658
execute if score #sq hr matches 659..720 run return run function rlk:boss/scarlet/seq/cs1/kb/659_720
