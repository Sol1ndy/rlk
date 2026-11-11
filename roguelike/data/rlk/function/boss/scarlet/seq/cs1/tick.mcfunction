# CS1 (hr_design §3.2): the clash, pushed apart, the hat and the bottle, the petal, 홍련일섬, the crimson field; locked 0-720, skippable 40-560 -> 566.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 720.
execute if score #sq hr matches 720.. run scoreboard players set #sqdone hr 1
scoreboard players set @a[tag=player] hudHold 2
execute if score #sq hr matches ..719 unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/cs1/lock
function rlk:boss/scarlet/seq/cs1/skipin
execute if score #sq_skn hr matches 1 run return run scoreboard players set #sq_skn hr 0
execute if score #sq hr matches 6..30 run return run function rlk:boss/scarlet/seq/cs1/kb/6_30
execute if score #sq hr matches 32..234 run return run function rlk:boss/scarlet/seq/cs1/kb/32_234
execute if score #sq hr matches 236..588 run return run function rlk:boss/scarlet/seq/cs1/kb/236_588
execute if score #sq hr matches 601..614 run return run function rlk:boss/scarlet/seq/cs1/kb/601_614
execute if score #sq hr matches 615..628 run return run function rlk:boss/scarlet/seq/cs1/kb/615_628
execute if score #sq hr matches 629..642 run return run function rlk:boss/scarlet/seq/cs1/kb/629_642
execute if score #sq hr matches 643..656 run return run function rlk:boss/scarlet/seq/cs1/kb/643_656
execute if score #sq hr matches 657..720 run return run function rlk:boss/scarlet/seq/cs1/kb/657_720
