# bomb clock 58
function rlk:mboss/fieldgen/rig_stub/play/slam
scoreboard players set #hzKB mb 4
scoreboard players set #hzVis mb 12
scoreboard players set #hzY1 mb 20
function rlk:mboss/hz/disc {r:50,tell:17,dmg:140}
playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.9 0.7 0.3
playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.6 1.5 0.2
execute at @s run particle minecraft:dust{color:[0.98f,0.871f,0.659f],scale:1.6} ~ ~4.2 ~ 0.12 0.05 0.12 0 2 force @a[tag=player]
execute at @s run particle minecraft:dust{color:[0.98f,0.871f,0.659f],scale:1.6} ~ ~3.15 ~ 0.12 0.05 0.12 0 2 force @a[tag=player]
execute at @s run particle minecraft:dust{color:[0.98f,0.871f,0.659f],scale:1.6} ~ ~2.1 ~ 0.12 0.05 0.12 0 2 force @a[tag=player]
execute at @s run particle minecraft:dust{color:[0.98f,0.871f,0.659f],scale:1.6} ~ ~1.05 ~ 0.12 0.05 0.12 0 2 force @a[tag=player]
execute at @s run particle minecraft:dust{color:[0.98f,0.871f,0.659f],scale:1.6} ~ ~0.21 ~ 0.12 0.05 0.12 0 2 force @a[tag=player]
