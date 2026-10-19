# sweep clock 31
# flame-trail segment 3 under her (group 2): a dark ember line, the flare 10 t later
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzAct mb 8
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 131
scoreboard players set #hzQuiet mb 1
execute positioned ~ 201 ~ rotated as @s rotated ~ 0 run function rlk:mboss/hz/disc {r:10,tell:10,dmg:20}
execute positioned ~ 201 ~ rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/tele/disc {r:10,tell:10,el:1,hold:8}
execute rotated as @s rotated ~ 0 positioned ~ ~0.05 ~ run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"~ ~ ~",rot:"~ 90",bb:"fixed",roll:0,spin:0,s0:1.6,s1:2,move:"0f,0f,0f",life:18,fade:6,col:14696512}
particle minecraft:dust{color:[0.549f,0.329f,0.212f],scale:1.2} ~ ~0.1 ~ 0.4 0.02 0.4 0 4 force @a[tag=player]
