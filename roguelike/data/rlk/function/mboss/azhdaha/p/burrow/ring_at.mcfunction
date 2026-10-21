# At a ring point: the hazard r 3.4 (own group) + its kit ring outline (keep), the ring sound, the shaft
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players set #hzEl mb 5
scoreboard players set #pjEl mb 5
function rlk:mboss/hz/disc {r:34,tell:19,dmg:50}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p9
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p9h
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p9ring
function rlk:mboss/azhdaha/fx/tele/chev_o {r:34,tell:19,el:5,nd:0,hold:3}
function rlk:mboss/azhdaha/fx/snd/burrow_ring
function rlk:mboss/azhdaha/fx/p/light_shaft
