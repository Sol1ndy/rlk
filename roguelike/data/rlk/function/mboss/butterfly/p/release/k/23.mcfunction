# release clock 23
# the cup: the dome r 10 at R, telegraphed 17 t (the decal and the hazard), the charge
scoreboard players set #hzEl mb 7
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p15r,limit=1] run function rlk:mboss/hz/disc {r:100,tell:17,dmg:130}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p15r,limit=1] run function rlk:mboss/butterfly/fx/tele/disc {r:100,tell:17,el:7,hold:4}
execute rotated as @s rotated ~ 0 positioned ^0 ^5.071 ^0.3 run function rlk:mboss/butterfly/fx/card {kind:"glow",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:1,s1:1.8,move:"0f,0f,0f",life:8,fade:3,col:14217916}
playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.23
playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.6 1.6 0.2
