# core choose, phase 0, as the boss at its feet (rdPat 0 on entry).
# 1. The forced first move after normal_return (TENMA tags it): sword -> 28 polearm, polearm -> 27 sword.
execute if entity @s[tag=rlk_rd_switch_due] if score @s rdWpn matches 0 run scoreboard players set @s rdPat 28
execute if entity @s[tag=rlk_rd_switch_due] if score @s rdWpn matches 1 run scoreboard players set @s rdPat 27
tag @s remove rlk_rd_switch_due
# 2. 몽상의 일심 always follows 찰나의 포영 (rdNext 7, set at its end or its stun end).
execute if score @s rdPat matches 0 if score @s rdNext matches 7 run scoreboard players set @s rdPat 7
# 3. The multi eye one pick after the single eye (rdSgEye 2 at the pick of 10).
execute if score @s rdPat matches 0 if score @s rdSgEye matches 1 run scoreboard players set @s rdPat 4
execute if score @s rdPat matches 0 if score @s rdSgEye matches 2.. run scoreboard players remove @s rdSgEye 1
# 4. Rear checks queued at the last pattern end, if the player is still behind her.
scoreboard players set #rdSgRear rd 0
execute if score @s rdPat matches 0 if score @s rdSgRearQ matches 1 at @s run function rlk:boss/raiden/sg/rear_test
execute if score @s rdPat matches 0 if score #rdSgRear rd matches 1 if score @s rdWpn matches 0 run scoreboard players set @s rdPat 25
execute if score @s rdPat matches 0 if score #rdSgRear rd matches 1 if score @s rdWpn matches 1 run scoreboard players set @s rdPat 26
scoreboard players set @s rdSgRearQ 0
# 5. The weapon bag with the range fit.
execute if score @s rdPat matches 0 if score @s rdWpn matches 0 at @s run function rlk:boss/raiden/sg/draw_0
execute if score @s rdPat matches 0 if score @s rdWpn matches 1 at @s run function rlk:boss/raiden/sg/draw_1
