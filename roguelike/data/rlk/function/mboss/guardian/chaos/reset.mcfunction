# End of a chaos cycle (groggy end, fail end, death, tests, reload): stars, sigil, streams, haze gone;
# both record slots reset (K22) and the looks back to gold.
kill @e[type=minecraft:husk,tag=rlk_mb_gd_star]
kill @e[tag=rlk_mb_gd_fx]
scoreboard players set #gdStars mb 0
scoreboard players set #gdSa1 mb 0
scoreboard players set #gdSa2 mb 0
scoreboard players set #gdCP mb 0
scoreboard players set #gdTim mb 0
scoreboard players set #gdTimS mb 0
scoreboard players set #gdHaze mb 0
scoreboard players set #gdBrk mb 0
scoreboard players set #gdFailDone mb 0
scoreboard players set #gdSlotA mb 0
scoreboard players set #gdSlotB mb 0
scoreboard players set #mbNoLeash mb 0
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/guardian/rig/eye/geo
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/guardian/rig/spear/geo
