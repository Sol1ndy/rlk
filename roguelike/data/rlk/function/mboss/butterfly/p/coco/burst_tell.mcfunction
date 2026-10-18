# @s = orb at the end of its homing: radial blades r 2.8 under it in 10 t, same group as the orb (one hit).
scoreboard players set @s mbPjV 1
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 1
scoreboard players operation #hzGrp mb = @s mbPjG
execute positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:28,tell:10,dmg:150}
