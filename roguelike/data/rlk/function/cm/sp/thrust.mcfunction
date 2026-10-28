# 찌르며 돌진 4틱(0.5칸/틱 = 2칸, 블록은 바닐라 물리로 막힘). 창끝 둘레(1.6칸 앞 r1.3 · 2.6칸 앞 r1.0)에 몸이 있으면 16, 창병 한 마리당 한 번 · 대열 전체로 한 틱 한 번
scoreboard players set #hold tmp 1
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
scoreboard players set #c2Fw tmp 500
scoreboard players set #c2Up tmp -1
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 run function rlk:cm/c2/impulse
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^1.2 ^2.0 run particle minecraft:crit ~ ~ ~ 0.25 0.05 0.25 0.1 3 normal
execute if score @s c2T2 matches 0 if score #c2SpHit tmp matches 0 rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^ ^1.6 if entity @e[tag=rlk_body,distance=..1.3] run function rlk:cm/sp/hit
execute if score @s c2T2 matches 0 if score #c2SpHit tmp matches 0 rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^ ^2.6 if entity @e[tag=rlk_body,distance=..1.0] run function rlk:cm/sp/hit
scoreboard players remove @s cmT 1
execute if score @s cmT matches ..0 run function rlk:cm/sp/end
