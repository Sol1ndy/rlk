data modify entity @e[tag=rlk_pm_weapon,limit=1] item set value {id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:player_motion/weapons/scythe"}}
data merge entity @e[tag=rlk_pm_weapon,limit=1] {brightness:{block:15,sky:15}}
scoreboard players set @s pmWModel 2
