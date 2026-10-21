# At the lock: own group, Pyro, KB 3; the seal8 decal = the hazard (keep, r 5.2, tell 28).
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
function rlk:mboss/hz/disc {r:52,tell:28,dmg:110}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p32h
function rlk:mboss/azhdaha/fx/tele/seal8_o {r:52,tell:28,el:1,hold:3}
function rlk:mboss/azhdaha/fx/snd/meteor_glyph
