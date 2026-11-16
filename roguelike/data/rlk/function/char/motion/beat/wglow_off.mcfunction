# @s = player. The weapon goes back to its own model and light.
execute unless score @s pbGlow matches 1 run return 0
scoreboard players set @s pbGlow 0
execute if score @s pmWModel matches 1 if score @s pmRigChar = #charN tmp run data merge entity @e[tag=rlk_pm_weapon,limit=1] {shadow_strength:1f,item:{components:{"minecraft:item_model":"rlk:player_motion/weapons/spear"}}}
execute if score @s pmWModel matches 1 if score @s pmRigChar = #charN tmp run data remove entity @e[tag=rlk_pm_weapon,limit=1] brightness
execute if score @s pmWModel matches 2 if score @s pmRigChar = #charN tmp run data merge entity @e[tag=rlk_pm_weapon,limit=1] {shadow_strength:1f,item:{components:{"minecraft:item_model":"rlk:player_motion/weapons/scythe"}}}
execute if score @s pmWModel matches 3 if score @s pmRigChar = #charN tmp run data merge entity @e[tag=rlk_pm_weapon,limit=1] {shadow_strength:1f,item:{components:{"minecraft:item_model":"rlk:player_motion/weapons/sword"}}}
execute if score @s pmWModel matches 3 if score @s pmRigChar = #charN tmp run data remove entity @e[tag=rlk_pm_weapon,limit=1] brightness
execute if score @s pmWModel matches 4 if score @s pmRigChar = #charN tmp run data merge entity @e[tag=rlk_pm_weapon,limit=1] {shadow_strength:1f,item:{components:{"minecraft:item_model":"rlk:player_motion/weapons/cryo_sword"}}}
execute if score @s pmWModel matches 5 if score @s pmRigChar = #charN tmp run data merge entity @e[tag=rlk_pm_weapon,limit=1] {shadow_strength:1f,item:{components:{"minecraft:item_model":"rlk:player_motion/weapons/navia_halberd"}}}
execute if score @s pmWModel matches 5 if score @s pmRigChar = #charN tmp run data remove entity @e[tag=rlk_pm_weapon,limit=1] brightness
execute if data entity @e[tag=rlk_pl_weapon,limit=1] {item:{components:{"minecraft:item_model":"rlk:player_motion/wg/iron_sword"}}} run data merge entity @e[tag=rlk_pl_weapon,limit=1] {shadow_strength:1f,item:{components:{"minecraft:item_model":"minecraft:iron_sword"}}}
execute if data entity @e[tag=rlk_pl_weapon,limit=1] {item:{components:{"minecraft:item_model":"rlk:player_motion/wg/diamond_sword"}}} run data merge entity @e[tag=rlk_pl_weapon,limit=1] {shadow_strength:1f,item:{components:{"minecraft:item_model":"minecraft:diamond_sword"}}}
execute if data entity @e[tag=rlk_pl_weapon,limit=1] {item:{components:{"minecraft:item_model":"rlk:player_motion/wg/netherite_sword"}}} run data merge entity @e[tag=rlk_pl_weapon,limit=1] {shadow_strength:1f,item:{components:{"minecraft:item_model":"minecraft:netherite_sword"}}}
execute if entity @e[tag=rlk_pl_weapon,limit=1] run data remove entity @e[tag=rlk_pl_weapon,limit=1] brightness
execute if score #charN tmp matches 7 if entity @e[tag=rlk_pl_weapon,limit=1] run data remove entity @e[tag=rlk_pl_weapon,limit=1] item
execute if score #charN tmp matches 7 as @e[tag=rlk_rncat] run data merge entity @s {Glowing:0b}
execute if score #charN tmp matches 8 if entity @e[tag=rlk_pl_weapon,limit=1] run data remove entity @e[tag=rlk_pl_weapon,limit=1] item
execute if score #charN tmp matches 8 as @e[tag=rlk_nfcat] run data merge entity @s {Glowing:0b}
