# Positioned at lump target 0: disc r 2.2, tell 26 (its flight), Pyro, the current volley group.
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 1
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
function rlk:mboss/hz/disc {r:22,tell:26,dmg:60}
