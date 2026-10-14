# Called by load. The minimap is the name of an invisible (white) boss bar.
scoreboard objectives add mm dummy
bossbar add rlk:minimap ""
bossbar set rlk:minimap color white
bossbar set rlk:minimap style progress
bossbar set rlk:minimap value 0
bossbar set rlk:minimap visible false
scoreboard players set #mmSig mm -1
# Rebuild the cell table once after a reload (a map made before it has none).
scoreboard players set #mmBuilt mm 0
execute unless score #mmX mm matches -1000..1000 run scoreboard players set #mmX mm -364
# New default position (version 2): the left edge at the top-left corner.
execute unless score #mmXv mm matches 2 run scoreboard players set #mmX mm -364
scoreboard players set #mmXv mm 2
