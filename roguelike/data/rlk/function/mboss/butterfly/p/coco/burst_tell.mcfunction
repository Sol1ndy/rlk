# @s = orb at the end of its homing (its pj ends in pj/all this tick: released, harmless): the burst
# hazard r 2.8 on the floor under it in its own volley group (one hit per orb; quiet: no
# decal), the beacon chime as it stops (its pulses follow on the orb itself).
scoreboard players operation #hzGrp mb = @s mbPjG
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:28,tell:10,dmg:100}
playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.4 1.9 0.13
