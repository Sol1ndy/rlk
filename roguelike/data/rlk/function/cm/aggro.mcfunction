# 두뇌는 미끼(또는 몸이 아닌 다른 것: 아이템 미끼)만 노린다. 몸이나 진짜 플레이어를 노리고 있으면 바로 미끼로 돌림
scoreboard players set #bad tmp 1
execute on target run scoreboard players set #bad tmp 0
execute on target if entity @s[type=minecraft:player] run scoreboard players set #bad tmp 1
execute on target if entity @s[tag=rlk_body] run scoreboard players set #bad tmp 1
execute if score #bad tmp matches 1 run function rlk:cm/aggro_force
