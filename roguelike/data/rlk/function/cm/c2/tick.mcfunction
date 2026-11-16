# 2챕터 두뇌 한 틱 (@s, at @s; cm/tick 에서, 플레이어가 쓰러져 있지 않을 때). #c2X = 이번 틱 가속 한 틱 더
scoreboard players add @s c2Age 1
scoreboard players set #c2X tmp 0
execute if entity @s[tag=rlk_cm_haste] run function rlk:cm/c2/haste_on
execute if entity @s[tag=rlk_c2hm,tag=!rlk_cm_haste] run function rlk:cm/c2/haste_off
execute if score @s c2Age matches 1 if entity @s[tag=rlk_c2a] run function rlk:cm/c2/first
execute if entity @s[tag=rlk_cm_ns] run return run function rlk:cm/ns/tick
execute if entity @s[tag=rlk_cm_sl] run return run function rlk:cm/sl/tick
execute if entity @s[tag=rlk_cm_ss] run return run function rlk:cm/ss/tick
execute if entity @s[tag=rlk_cm_sp] run return run function rlk:cm/sp/tick
execute if entity @s[tag=rlk_cm_dr] run return run function rlk:cm/dr/tick
