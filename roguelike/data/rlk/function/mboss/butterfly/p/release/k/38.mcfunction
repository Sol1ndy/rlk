# release clock 38
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 4
execute positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:100,tell:15,dmg:260}
playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.8 1.4 0.27
