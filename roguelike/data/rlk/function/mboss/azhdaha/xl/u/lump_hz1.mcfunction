# Positioned at lump target 1: disc r 2.2, tell 27 (its flight), Pyro, the current volley group.
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 1
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
function rlk:mboss/hz/disc {r:22,tell:27,dmg:60}
