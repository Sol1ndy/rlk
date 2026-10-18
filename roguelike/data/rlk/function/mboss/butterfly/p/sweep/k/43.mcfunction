# sweep clock 43
function rlk:mboss/mv/step {d:0.3}
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
execute positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:10,tell:10,dmg:30}
particle minecraft:flame ~ ~0.3 ~ 0.4 0.1 0.4 0.01 6 force @a[tag=player]
