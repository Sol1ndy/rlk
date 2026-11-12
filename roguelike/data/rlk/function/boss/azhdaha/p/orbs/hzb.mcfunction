# @s = the orb's hazard: its height band (milliblocks) by #aq31H.
execute if score #aq31H mb matches 0 run scoreboard players set @s mbHzY0 0
execute if score #aq31H mb matches 0 run scoreboard players set @s mbHzY1 2200
execute if score #aq31H mb matches 1 run scoreboard players set @s mbHzY0 2600
execute if score #aq31H mb matches 1 run scoreboard players set @s mbHzY1 4600
execute if score #aq31H mb matches 2 run scoreboard players set @s mbHzY0 99000
execute if score #aq31H mb matches 2 run scoreboard players set @s mbHzY1 99000
