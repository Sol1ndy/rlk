scoreboard players remove #azArT mb 4
scoreboard players remove @e[type=minecraft:item_display,tag=rlk_mb_az_ap,scores={azT=1..}] azT 4
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_ap,scores={azT=..0}] run function rlk:boss/azhdaha/arena/look_one
scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_az_ap,scores={azT=..0}] azT -1000
