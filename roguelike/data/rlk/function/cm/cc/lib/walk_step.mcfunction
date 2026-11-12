scoreboard players set #wOk tmp 0
# flat / one down / one up; the body also needs 0.3 b of room on both sides (no corner squeezing)
execute if block ^ ^0.3 ^0.5 #rlk:dash_pass if block ^ ^1.2 ^0.5 #rlk:dash_pass if block ^ ^1.85 ^0.5 #rlk:dash_pass unless block ^ ^-0.5 ^0.5 #rlk:cm_pass if block ^0.3 ^1 ^0.5 #rlk:dash_pass if block ^-0.3 ^1 ^0.5 #rlk:dash_pass run scoreboard players set #wOk tmp 1
execute if score #wOk tmp matches 0 if block ^ ^0.3 ^0.5 #rlk:dash_pass if block ^ ^1.2 ^0.5 #rlk:dash_pass if block ^ ^1.85 ^0.5 #rlk:dash_pass if block ^ ^-0.5 ^0.5 #rlk:cm_pass unless block ^ ^-1.5 ^0.5 #rlk:cm_pass if block ^0.3 ^0.2 ^0.5 #rlk:dash_pass if block ^-0.3 ^0.2 ^0.5 #rlk:dash_pass run scoreboard players set #wOk tmp 2
execute if score #wOk tmp matches 0 unless block ^ ^0.3 ^0.5 #rlk:cm_pass if block ^ ^1.3 ^0.5 #rlk:dash_pass if block ^ ^2.2 ^0.5 #rlk:dash_pass if block ^ ^2.85 ^0.5 #rlk:dash_pass if block ~ ~2.85 ~ #rlk:dash_pass if block ^0.3 ^2 ^0.5 #rlk:dash_pass if block ^-0.3 ^2 ^0.5 #rlk:dash_pass run scoreboard players set #wOk tmp 3
execute if score #wOk tmp matches 0 run return 0
execute if score #wOk tmp matches 1 run tp @s ^ ^ ^0.5
execute if score #wOk tmp matches 2 run tp @s ^ ^-1 ^0.5
execute if score #wOk tmp matches 3 run tp @s ^ ^1 ^0.5
scoreboard players add #wK tmp 1
scoreboard players remove #wN tmp 1
execute if score #wN tmp matches 1.. at @s run function rlk:cm/cc/lib/walk_step
