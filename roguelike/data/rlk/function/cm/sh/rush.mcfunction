# 돌진: 0.35칸 × 2 × 20틱 = 14칸. 플레이어에 닿아도 계속 돌진하며, 통과할 수 없는 벽에서만 조기 종료
scoreboard players set #hold tmp 1
scoreboard players remove @s cmT 1
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
scoreboard players set #rs tmp 2
function rlk:cm/sh/rstep
particle minecraft:cloud ~ ~0.1 ~ 0.3 0 0.3 0.02 2
scoreboard players operation #t1 tmp = @s cmT
scoreboard players operation #t1 tmp %= #3 tmp
execute if score #t1 tmp matches 0 unless score #k96 snd matches 1 run function rlk:snd/f103
execute if score @s cmS matches 3 if score @s cmT matches ..0 run function rlk:cm/sh/rend
