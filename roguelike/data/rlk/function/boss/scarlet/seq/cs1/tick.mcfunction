# CS1 (hr_design §3.2): the clash, pushed apart, the hat and the bottle, the petal, 홍련일섬, the crimson field; locked 0-720, skippable 40-560 -> 566.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 720.
execute if score #sq hr matches 720.. run scoreboard players set #sqdone hr 1
scoreboard players set @a[tag=player] hudHold 2
execute if score #sq hr matches ..719 unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/cs1/lock
execute if score #sq hr matches 6..21 run return run function rlk:boss/scarlet/seq/cs1/kb/6_21
execute if score #sq hr matches 22..186 run return run function rlk:boss/scarlet/seq/cs1/kb/22_186
execute if score #sq hr matches 200..591 run return run function rlk:boss/scarlet/seq/cs1/kb/200_591
execute if score #sq hr matches 592..601 run return run function rlk:boss/scarlet/seq/cs1/kb/592_601
execute if score #sq hr matches 602..620 run return run function rlk:boss/scarlet/seq/cs1/kb/602_620
execute if score #sq hr matches 621..651 run return run function rlk:boss/scarlet/seq/cs1/kb/621_651
execute if score #sq hr matches 652..661 run return run function rlk:boss/scarlet/seq/cs1/kb/652_661
execute if score #sq hr matches 662..720 run return run function rlk:boss/scarlet/seq/cs1/kb/662_720
