# N17 / plan 2.6: the arena props to the geo element look as a wave from the boss outward over 20 t.
scoreboard players set #azArEl mb 5
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_az_ap] azT 20
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_az_ap,distance=..7] azT 5
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_az_ap,distance=..14] azT 10
execute at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_az_ap,distance=..21] azT 15
scoreboard players set #azArT mb 21
