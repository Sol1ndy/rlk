# @s = the attacker of a mboss/hurt call (hazard marker, prop, body). The one-shot hit context of player/def/judge.
tag @e[tag=rlk_hc_atk] remove rlk_hc_atk
scoreboard players set #hcC tmp 2
scoreboard players set #hcK tmp 1
execute if score #mbSrcIn mb matches 2 run scoreboard players set #hcK tmp 2
execute if score #mbSrcIn mb matches 1 if score @s mbHzK matches 2 run scoreboard players set #hcK tmp 3
execute if score #mbSrcIn mb matches 1 if score @s mbHzK matches 5..6 run scoreboard players set #hcK tmp 3
scoreboard players operation #hcND tmp = #mbNoDodge mb
scoreboard players operation #hcNP tmp = #mbNoParry mb
tag @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] add rlk_hc_atk
