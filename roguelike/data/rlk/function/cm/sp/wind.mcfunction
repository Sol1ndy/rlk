# 창끝 빛(1초): 방향 고정, 경직 · 빙결이면 취소
scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return run function rlk:cm/cancel
execute if entity @s[tag=rlk_c2fresh] run return 0
scoreboard players remove @s cmT 1
execute if score #c2X tmp matches 1 run scoreboard players remove @s cmT 1
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^-0.25 ^1.15 ^1.55 run particle minecraft:electric_spark ~ ~ ~ 0.04 0.04 0.04 0.02 1 normal
execute if score @s cmT matches ..0 run function rlk:cm/sp/go
