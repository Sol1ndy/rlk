# Orb 0: ring 1 (r 6.5, -3.5 deg/t), angle = base + 0 + omega x #aq31C; Hydro hz r 1.3
# (N5 orb/spawn: band, #hzRearm 10, the current volley group); its prop; ring and pattern tags.
scoreboard players set #aq31O mb -350
scoreboard players operation #aq31Q mb = #aq31C mb
scoreboard players operation #aq31Q mb *= #aq31O mb
scoreboard players operation #aq31Q mb += #aq31A mb
scoreboard players add #aq31Q mb 0
scoreboard players set #hzEl mb 2
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
data modify storage rlk:mboss az.orb set value {tag:"rlk_mb_az_p31o0",ring:1,a:4500,r:6500,w:-350,hr:13,y0:0,y1:22,dmg:29,grp:1}
execute store result storage rlk:mboss az.orb.a int 1 run scoreboard players get #aq31Q mb
function rlk:mboss/azhdaha/orb/spawn with storage rlk:mboss az.orb
tag @e[type=minecraft:marker,tag=rlk_mb_az_p31o0] add rlk_mb_az_p31o
tag @e[type=minecraft:marker,tag=rlk_mb_az_p31o0] add rlk_mb_az_p31r1
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p31o0,limit=1] run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p31","rlk_mb_az_p31d","rlk_mb_az_p31d0"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p31d0,limit=1] run function rlk:mboss/azhdaha/p/orbs/dress
