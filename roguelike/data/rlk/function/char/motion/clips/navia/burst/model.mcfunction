# Generated: the weapon model in force at pmTick (@s player; after a respawn inside the clip).
execute if score @s pmTick matches 0..42 run data modify entity @e[tag=rlk_pm_weapon,limit=1] item set value {id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:player_motion/weapons/navia_parasol_open"}}
execute if score @s pmTick matches 0..42 run data remove entity @e[tag=rlk_pm_weapon,limit=1] brightness
execute if score @s pmTick matches 0..42 run scoreboard players set @s pmWModel 7
execute if score @s pmTick matches 43..47 run data modify entity @e[tag=rlk_pm_weapon,limit=1] item set value {id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:player_motion/weapons/navia_parasol"}}
execute if score @s pmTick matches 43..47 run data remove entity @e[tag=rlk_pm_weapon,limit=1] brightness
execute if score @s pmTick matches 43..47 run scoreboard players set @s pmWModel 6
execute if score @s pmTick matches 48..54 run data modify entity @e[tag=rlk_pm_weapon,limit=1] item set value {id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:player_motion/weapons/navia_halberd"}}
execute if score @s pmTick matches 48..54 run data remove entity @e[tag=rlk_pm_weapon,limit=1] brightness
execute if score @s pmTick matches 48..54 run scoreboard players set @s pmWModel 5
