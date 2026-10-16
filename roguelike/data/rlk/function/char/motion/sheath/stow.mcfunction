# Quick stow: gold sparkle at the hand, the weapon vanishes, then grows on the back (sheath/fx_tick).
execute unless score @s pmSheath matches 1 if entity @e[tag=rlk_pm_weapon] run scoreboard players set @s pmShFx 8
execute unless score @s pmSheath matches 1 if entity @e[tag=rlk_pm_weapon] run data merge entity @e[tag=rlk_pm_weapon,limit=1] {start_interpolation:0,interpolation_duration:0,transformation:{scale:[0f,0f,0f]}}
execute unless score @s pmSheath matches 1 if entity @e[tag=rlk_pm_weapon] if score #charN tmp matches 5 at @e[tag=rlk_pm_body,limit=1] rotated as @e[tag=rlk_pm_body,limit=1] positioned ^-0.421 ^0.833 ^0.149 run function rlk:char/motion/sheath/fx_hand
execute unless score @s pmSheath matches 1 if entity @e[tag=rlk_pm_weapon] if score #charN tmp matches 3 at @e[tag=rlk_pm_body,limit=1] rotated as @e[tag=rlk_pm_body,limit=1] positioned ^-0.439 ^0.838 ^0.165 run function rlk:char/motion/sheath/fx_hand
execute unless score @s pmSheath matches 1 if entity @e[tag=rlk_pm_weapon] at @e[tag=rlk_pm_body,limit=1] run playsound minecraft:item.armor.equip_iron player @s ~ ~1 ~ 0.35 1.5 0
scoreboard players set @s pmSheath 1
scoreboard players set @s pmShT 0
