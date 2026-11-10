# CS1 (hr_design §3.2): the clash, pushed apart, the hat and the bottle, the petal, 홍련일섬, the crimson field; locked 0-720, skippable 40-560 -> 566.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 720.
execute if score #sq hr matches 720.. run scoreboard players set #sqdone hr 1
scoreboard players set @a[tag=player] hudHold 2
execute if score #sq hr matches ..719 unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/cs1/lock
execute if score #sq hr matches 6..20 run return run function rlk:boss/scarlet/seq/cs1/kb/6_20
execute if score #sq hr matches 21..110 run return run function rlk:boss/scarlet/seq/cs1/kb/21_110
execute if score #sq hr matches 180..500 run return run function rlk:boss/scarlet/seq/cs1/kb/180_500
execute if score #sq hr matches 578..597 run return run function rlk:boss/scarlet/seq/cs1/kb/578_597
execute if score #sq hr matches 598..606 run return run function rlk:boss/scarlet/seq/cs1/kb/598_606
execute if score #sq hr matches 610..651 run return run function rlk:boss/scarlet/seq/cs1/kb/610_651
execute if score #sq hr matches 652..660 run return run function rlk:boss/scarlet/seq/cs1/kb/652_660
execute if score #sq hr matches 661..720 run return run function rlk:boss/scarlet/seq/cs1/kb/661_720
