# Positioned at the centre: the heptagram (keep, r 7.5, tell 22) and its hazard disc (same size and
# tell), Cryo (the tail element) + a stack, own volley group; the draw sound.
function rlk:mboss/azhdaha/fx/tele/heptagram_o {r:75,tell:22,el:4,hold:3}
function rlk:mboss/azhdaha/fx/snd/frost_draw
scoreboard players operation #aq41B mb = #azB3T mb
scoreboard players add #aq41B mb 22
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 411
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzEl mb = #azET mb
scoreboard players operation #pjEl mb = #azET mb
function rlk:mboss/hz/disc {r:75,tell:22,dmg:79}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p41
