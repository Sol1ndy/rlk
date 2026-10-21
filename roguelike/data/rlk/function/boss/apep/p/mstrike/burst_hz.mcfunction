# At L: the burst (quiet hazard + the kit decal of the keep row) and the rosette.
scoreboard players set #hzEl mb 7
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
function rlk:mboss/hz/disc {r:42,tell:12,dmg:140}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_p31k
function rlk:boss/apep/fx/tele/disc_o {r:42,tell:12,el:7,nd:0,hold:3}
function rlk:boss/apep/fx/p/rosette
function rlk:boss/apep/fx/snd/q1_rosette
