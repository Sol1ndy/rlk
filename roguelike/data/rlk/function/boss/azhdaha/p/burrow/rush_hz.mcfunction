# At the breach point: the rush hazard (moved onto the body from its hit on)
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzAct mb 21
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players set #hzEl mb 5
scoreboard players set #pjEl mb 5
function rlk:mboss/hz/disc {r:30,tell:20,dmg:58}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p9
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p9h
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p9rush
function rlk:boss/azhdaha/fx/p/mound
function rlk:boss/azhdaha/fx/snd/burrow_loop
