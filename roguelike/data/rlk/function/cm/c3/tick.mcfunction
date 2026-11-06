# 3챕터 두뇌 한 틱 (@s, at @s; cm/tick 에서, 플레이어가 쓰러져 있지 않을 때). 정예(B)는 자기 연결 줄로 돈다
scoreboard players add @s c2Age 1
execute if score @s c2Age matches 1 if entity @s[tag=rlk_c3a] run function rlk:cm/c2/first
execute if entity @s[tag=rlk_cm_fu] run return run function rlk:cm/fu/tick
execute if entity @s[tag=rlk_cm_em] run return run function rlk:cm/em/tick
execute if entity @s[tag=rlk_cm_sb] run return run function rlk:cm/sb/tick
execute if entity @s[tag=rlk_cm_cw] run return run function rlk:cm/cw/tick
