# jump clock 3
function rlk:mboss/butterfly/rig/face/track
scoreboard players set #hzAct mb 4
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzY1 mb 10
execute positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:30,tell:10,dmg:90}
execute positioned ~ 201 ~ run function rlk:mboss/butterfly/fx/tele/disc {r:30,tell:10,el:7,hold:3}
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.35 1.6 0.12
