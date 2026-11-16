# Fail +5 (m4 +7): stars flash white, their husks (and HP bars) go.
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_starv] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/guardian/star_flash"
kill @e[type=minecraft:husk,tag=rlk_mb_gd_star]
scoreboard players set #gdStars mb 0
