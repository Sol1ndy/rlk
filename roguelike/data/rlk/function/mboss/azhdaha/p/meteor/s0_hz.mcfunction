# At target 0: disc r 2.8, tell 12, Pyro, the group of the six; no ground decal
# (Change note 1): the halo in the air and the falling meteor are the tell.
function rlk:mboss/grp_new
scoreboard players operation #aq32G mb = #mbGrp mb
scoreboard players set #hzEl mb 1
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzGrp mb = #aq32G mb
function rlk:mboss/hz/disc {r:28,tell:12,dmg:66}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p32h
function rlk:mboss/azhdaha/fx/tele/halo {r:28,h:30,tell:12,el:1,hold:2}
summon minecraft:item_display ~ ~16 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p32","rlk_mb_az_p32p0"],teleport_duration:0}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p32p0,limit=1] run function rlk:mboss/azhdaha/fx/prop/meteor_small
