# @s = body (emerged at the centre): face the target, growl; the run length #aq9R = dist + 4 b (<= 24 t); the
# run disc r 4 rides the body from its first hit (tell 20); the pattern end = the run end + charge_stop.
function rlk:mboss/mv/face
function rlk:mboss/azhdaha/fx/snd/charge_growl
function rlk:mboss/mv/dist
scoreboard players operation #aq9R mb = #mbDist mb
scoreboard players add #aq9R mb 49
scoreboard players operation #aq9R mb /= #azK10 mb
execute if score #aq9R mb matches 25.. run scoreboard players set #aq9R mb 24
scoreboard players operation #aq9X mb = #aq9R mb
scoreboard players add #aq9X mb 280
scoreboard players operation #azPLen mb = #aq9X mb
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzAct mb 25
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players set #hzEl mb 5
scoreboard players set #pjEl mb 5
function rlk:mboss/hz/disc {r:40,tell:20,dmg:45}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p9
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p9h
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p9run
