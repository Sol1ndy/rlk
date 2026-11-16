# @s = a new hazard made with #hzPm mb (cm.md 13.11): its hit takes mbHzPm per mille (1..1000) of the player's max HP
# through mboss/pl_dot; lethal unless #hzPmL mb 0 (unset = 1), which is spent here.
scoreboard players operation @s mbHzPm = #hzPm mb
execute if score @s mbHzPm matches 1001.. run scoreboard players set @s mbHzPm 1000
scoreboard players set @s mbHzPmL 1
execute if score #hzPmL mb matches 0 run scoreboard players set @s mbHzPmL 0
scoreboard players reset #hzPmL mb
