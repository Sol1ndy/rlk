# 4틱마다 대열 유지: 가운데(c2R 1)의 방향 기준 왼쪽(^1.7)/오른쪽(^-1.7) 자리로 끌림. 가운데가 없으면 내가 가운데
scoreboard players set @s c2T 4
execute if score @s c2R matches 1 run return 0
scoreboard players operation #g tmp = @s c2G
execute as @e[tag=rlk_cm_sp,distance=..12] if score @s c2G = #g tmp if score @s c2R matches 1 run tag @s add rlk_c2ld
execute unless entity @e[tag=rlk_c2ld,limit=1] run return run scoreboard players set @s c2R 1
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @e[tag=rlk_c2ld,limit=1] cmYaw
scoreboard players set #c2Fw tmp 180
scoreboard players set #c2Up tmp -1
execute if score @s c2R matches 0 at @e[tag=rlk_c2ld,limit=1] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^1.7 ^ ^ unless entity @s[distance=..0.8] facing entity @s feet rotated ~180 0 run function rlk:cm/c2/impulse
execute if score @s c2R matches 2 at @e[tag=rlk_c2ld,limit=1] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^-1.7 ^ ^ unless entity @s[distance=..0.8] facing entity @s feet rotated ~180 0 run function rlk:cm/c2/impulse
tag @e[tag=rlk_c2ld] remove rlk_c2ld
