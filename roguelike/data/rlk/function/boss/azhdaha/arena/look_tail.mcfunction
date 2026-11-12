# N17 / plan 2.6: the arena props to the tail element look as a wave from the boss outward over 20 t.
scoreboard players operation #azArEl mb = #azTail mb
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_az_ap] azT 20
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_az_ap,distance=..7] azT 5
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_az_ap,distance=..14] azT 10
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_az_ap,distance=..21] azT 15
scoreboard players set #azArT mb 21
execute if score #azArEl mb matches 1 at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:boss/azhdaha/fx/p/recolour/1 {r:2800,t:20}
execute if score #azArEl mb matches 2 at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:boss/azhdaha/fx/p/recolour/2 {r:2800,t:20}
execute if score #azArEl mb matches 3 at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:boss/azhdaha/fx/p/recolour/3 {r:2800,t:20}
execute if score #azArEl mb matches 4 at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:boss/azhdaha/fx/p/recolour/4 {r:2800,t:20}
