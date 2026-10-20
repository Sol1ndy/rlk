# At the geyser spot: own volley group, Hydro, the swirl decal = the hazard (r, tell).
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 2
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
function rlk:mboss/hz/disc {r:30,tell:22,dmg:80}
function rlk:mboss/azhdaha/fx/tele/disc_o {r:30,tell:22,el:2,nd:0,hold:3}
playsound minecraft:block.bubble_column.whirlpool_inside hostile @a[tag=player] ~ ~ ~ 0.9 1.1 0.3
scoreboard players set #azAftF mb 1
scoreboard players set #azAftD mb 22
function rlk:mboss/azhdaha/aft/new
