# Fail +7: stars flash white, their husks (and HP bars) go.
execute as @e[type=minecraft:text_display,tag=rlk_mb_gd_starv] run data merge entity @s {text:{text:"✦",color:"#FFFFFF"}}
kill @e[type=minecraft:husk,tag=rlk_mb_gd_star]
scoreboard players set #gdStars mb 0
