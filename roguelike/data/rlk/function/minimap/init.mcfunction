# Called by load. The minimap is the name of an invisible (white) boss bar.
scoreboard objectives add mm dummy
bossbar add rlk:minimap ""
bossbar set rlk:minimap color white
bossbar set rlk:minimap style progress
bossbar set rlk:minimap value 0
bossbar set rlk:minimap visible false
scoreboard players set #mmSig mm -1
