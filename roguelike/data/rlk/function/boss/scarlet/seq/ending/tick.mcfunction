# The ending (hr_design §3.5): she rises, the clash, the aerial duel, the landing, the sheathe, lines 17-23, the hat tip; H at its end; locked from tick 0 into the coda.
# Tick (@s = the body; #sq hr 1.. = the clip tick shown this game tick); #sqdone at 1372.
execute if score #sq hr matches 1372.. run scoreboard players set #sqdone hr 1
scoreboard players set @a[tag=player] hudHold 2
execute if score #sq hr matches ..1372 unless score #sq_cx hr matches 1 run function rlk:boss/scarlet/seq/ending/lock
execute if score #sq hr matches 6..120 run return run function rlk:boss/scarlet/seq/ending/kb/6_120
execute if score #sq hr matches 121..266 run return run function rlk:boss/scarlet/seq/ending/kb/121_266
execute if score #sq hr matches 286..428 run return run function rlk:boss/scarlet/seq/ending/kb/286_428
execute if score #sq hr matches 430..486 run return run function rlk:boss/scarlet/seq/ending/kb/430_486
execute if score #sq hr matches 488..716 run return run function rlk:boss/scarlet/seq/ending/kb/488_716
execute if score #sq hr matches 718..924 run return run function rlk:boss/scarlet/seq/ending/kb/718_924
execute if score #sq hr matches 926..1118 run return run function rlk:boss/scarlet/seq/ending/kb/926_1118
execute if score #sq hr matches 1120..1318 run return run function rlk:boss/scarlet/seq/ending/kb/1120_1318
