# Generated: the weapon model in force at pmTick (@s player; after a respawn inside the clip).
execute if score @s pmTick matches 0 run data modify entity @e[tag=rlk_pm_weapon,limit=1] item set value {id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:player_motion/weapons/navia_parasol"}}
execute if score @s pmTick matches 0 run data remove entity @e[tag=rlk_pm_weapon,limit=1] brightness
execute if score @s pmTick matches 0 run scoreboard players set @s pmWModel 6
execute if score @s pmTick matches 1..14 run data modify entity @e[tag=rlk_pm_weapon,limit=1] item set value {id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:player_motion/weapons/navia_parasol_open"}}
execute if score @s pmTick matches 1..14 run data remove entity @e[tag=rlk_pm_weapon,limit=1] brightness
execute if score @s pmTick matches 1..14 run scoreboard players set @s pmWModel 7
execute if score @s pmTick matches 15..17 run data modify entity @e[tag=rlk_pm_weapon,limit=1] item set value {id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:player_motion/weapons/navia_parasol"}}
execute if score @s pmTick matches 15..17 run data remove entity @e[tag=rlk_pm_weapon,limit=1] brightness
execute if score @s pmTick matches 15..17 run scoreboard players set @s pmWModel 6
execute if score @s pmTick matches 18..24 run data modify entity @e[tag=rlk_pm_weapon,limit=1] item set value {id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:player_motion/weapons/navia_halberd"}}
execute if score @s pmTick matches 18..24 run data remove entity @e[tag=rlk_pm_weapon,limit=1] brightness
execute if score @s pmTick matches 18..24 run scoreboard players set @s pmWModel 5
