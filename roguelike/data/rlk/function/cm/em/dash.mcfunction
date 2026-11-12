# 돌진 찌르기 (0.6칸/틱, 블록은 바닐라 물리로 막힘). 단검 끝(0.8칸 앞 r1.3)에 몸이 있으면 14, 용병 한 마리당 한 번 · 무리 전체로 한 틱 한 번
scoreboard players set #hold tmp 1
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
scoreboard players set #c2Fw tmp 600
scoreboard players set #c2Up tmp -1
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 run function rlk:cm/c2/impulse
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^0.9 ^0.8 run particle minecraft:crit ~ ~ ~ 0.2 0.1 0.2 0.1 2 normal
execute if score @s c2T2 matches 0 if score #c3EmHit tmp matches 0 rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^ ^0.8 if entity @e[tag=rlk_body,distance=..1.3] run function rlk:cm/em/hit
scoreboard players remove @s cmT 1
execute if score @s cmT matches ..0 run function rlk:cm/em/end
