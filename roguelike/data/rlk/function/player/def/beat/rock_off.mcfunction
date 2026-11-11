# 젖혀 둔 부품을 제자리로(6틱, 세계의 틱보다 먼저: 그 틱의 리그가 다시 자리를 잡는다). 모듈의 자기 자세도 되돌리게 한다
scoreboard players set #btRk cb 0
execute as @e[tag=rlk_bt_rk] at @s rotated ~ 0 run tp @s ^ ^-0.06 ^0.2 ~ 0
tag @e[tag=rlk_bt_rk] remove rlk_bt_rk
execute as @e[type=minecraft:husk,tag=rlk_mb_body,tag=rlk_bt_atk,limit=1] at @s run function rlk:mboss/d/beat_release
