# sweep clock 27
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p13p,limit=1] positioned ^ ^0.4 ^2.2 run particle minecraft:dust{color:[0.929f,0.765f,0.043f],scale:0.8} ~ ~ ~ 2.2 0.4 1.2 0 10 force @a[tag=player]
# flame-trail segment 1 under her (group 1): the red ember line (the footage's flame line,
# the only ground visual before its flare: TRIM, no disc decal) up to the flare 10 t later
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzAct mb 8
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 131
scoreboard players set #hzQuiet mb 1
execute positioned ~ 201 ~ rotated as @s rotated ~ 0 run function rlk:mboss/hz/disc {r:10,tell:10,dmg:20}
execute rotated as @s rotated ~ 0 positioned ~ ~0.05 ~ run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"~ ~ ~",rot:"~ 90",bb:"fixed",roll:0,spin:0,s0:1.6,s1:2,move:"0f,0f,0f",life:11,fade:3,col:14696512}
particle minecraft:dust{color:[0.549f,0.329f,0.212f],scale:1.2} ~ ~0.1 ~ 0.4 0.02 0.4 0 4 force @a[tag=player]
