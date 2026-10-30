# Nova resume (the kit swell cards were cleared on pause): the swell for the rest of its time.
execute unless score #pt tk matches ..39 run return 0
scoreboard players set #mantle_t tk 40
scoreboard players operation #mantle_t tk -= #pt tk
data modify storage rlk:tk air.nova set value {t:1}
execute store result storage rlk:tk air.nova.t int 1 run scoreboard players get #mantle_t tk
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s rotated as @s rotated ~ 0 positioned ~ ~1.75 ~ run function rlk:boss/tachy/fx/p/nova_swell with storage rlk:tk air.nova
