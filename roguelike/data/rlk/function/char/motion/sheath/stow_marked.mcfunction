# Gold sparkle at the marked position, the weapon vanishes, then re-forms on the back (sheath/fx_tick).
execute unless score @s pmSheath matches 1 if entity @e[tag=rlk_pm_weapon] run scoreboard players set @s pmShFx 8
execute unless score @s pmSheath matches 1 if entity @e[tag=rlk_pm_weapon] run data merge entity @e[tag=rlk_pm_weapon,limit=1] {start_interpolation:0,interpolation_duration:0,transformation:{scale:[0f,0f,0f]}}
execute unless score @s pmSheath matches 1 if entity @e[tag=rlk_pm_weapon] run function rlk:char/motion/sheath/spark with storage rlk:player_motion spark
execute unless score @s pmSheath matches 1 if entity @e[tag=rlk_pm_weapon] at @e[tag=rlk_pm_body,limit=1] run playsound minecraft:item.armor.equip_iron player @s ~ ~1 ~ 0.35 1.5 0
scoreboard players set @s pmSheath 1
scoreboard players set @s pmShT 0
