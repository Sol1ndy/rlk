scoreboard players set #hold tmp 1
scoreboard players remove @s cmT 1
# Ignite only after the hand reaches the fuse; smoke is attached to the larger breech.
scoreboard players operation #cnFuse tmp = #cmW_cn tmp
scoreboard players set #cnDiv tmp 5
scoreboard players operation #cnFuse tmp *= #2 tmp
scoreboard players operation #cnFuse tmp /= #cnDiv tmp
execute if score @s cmT <= #cnFuse tmp facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^1.47 ^-0.55 run particle minecraft:smoke ~ ~ ~ 0.025 0.025 0.025 0.01 2
execute if score @s cmT <= #cnFuse tmp facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^1.47 ^-0.55 run particle minecraft:small_flame ~ ~ ~ 0.015 0.02 0.015 0.005 1
execute if score @s cmT matches ..0 run function rlk:cm/cn/fire
