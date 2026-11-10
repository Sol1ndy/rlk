# The ending (hr_design §3.5): she rises, the clash, the aerial duel, the landing, the sheathe, lines 17-23, the hat tip; H at its end; locked from tick 0 into the coda.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 1372.
execute if score #sq hr matches 1372.. run scoreboard players set #sqdone hr 1
scoreboard players set @a[tag=player] hudHold 2
execute if score #sq hr matches ..1372 unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/ending/lock
execute if score #sq hr matches 6..68 run return run function rlk:boss/scarlet/seq/ending/kb/6_68
execute if score #sq hr matches 70..120 run return run function rlk:boss/scarlet/seq/ending/kb/70_120
execute if score #sq hr matches 121..182 run return run function rlk:boss/scarlet/seq/ending/kb/121_182
execute if score #sq hr matches 186..298 run return run function rlk:boss/scarlet/seq/ending/kb/186_298
execute if score #sq hr matches 314..432 run return run function rlk:boss/scarlet/seq/ending/kb/314_432
execute if score #sq hr matches 433..657 run return run function rlk:boss/scarlet/seq/ending/kb/433_657
execute if score #sq hr matches 658..1081 run return run function rlk:boss/scarlet/seq/ending/kb/658_1081
execute if score #sq hr matches 1082..1300 run return run function rlk:boss/scarlet/seq/ending/kb/1082_1300
