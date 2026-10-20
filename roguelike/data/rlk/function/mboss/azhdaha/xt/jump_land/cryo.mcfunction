# Cryo frost ring (plan 4.6): r 1.5 -> 6.0 at 0.75 b/t, band 1.5, from E+2, x_cring + a Cryo stack;
# no pre-strike decal (Change note 1): the host impact and the travelling front are the read.
scoreboard players set #hzAct mb 7
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players set #hzY1 mb 7
scoreboard players operation #hzGrp mb = #azCtxGrp mb
scoreboard players operation #hzEl mb = #azET mb
scoreboard players operation #pjEl mb = #azET mb
function rlk:mboss/hz/ring {r0:0,r:15,tell:14,dmg:60}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_x
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_xcr
execute as @e[type=minecraft:marker,tag=rlk_mb_az_xcr] if score @s mbHzI = #hzLast mb run scoreboard players set @s azT 0
scoreboard players set #azAftF mb 3
scoreboard players set #azAftD mb 13
function rlk:mboss/azhdaha/aft/new
