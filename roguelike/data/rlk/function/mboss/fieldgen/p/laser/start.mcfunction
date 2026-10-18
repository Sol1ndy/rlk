# C3 코어 (clip laser; @s = body; the yaw never changes): two beams made at 0 (tell 24), active 133 t, the rig orbit 5 / -5 deg/t from 24; meets [42, 78, 114, 150].
scoreboard players set #fq3Pz mb 0
function rlk:mboss/grp_new
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p3e]
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p3g]
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzAct mb 133
scoreboard players set #hzKB mb 2
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 31
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzRearm mb 10
scoreboard players set #hzY0 mb -5
scoreboard players set #hzY1 mb 20
execute at @s rotated as @s rotated ~-90 0 positioned ^ ^ ^3 run function rlk:mboss/hz/line {len:28,w:6,tell:24,dmg:50}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_fg_p3e
execute at @s rotated as @s rotated ~-90 0 positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/tele/mline {id:0,len:58,w:6,back:-30,tell:24,el:5,hold:133}
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzAct mb 133
scoreboard players set #hzKB mb 2
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 31
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzRearm mb 10
scoreboard players set #hzY0 mb -5
scoreboard players set #hzY1 mb 20
execute at @s rotated as @s rotated ~90 0 positioned ^ ^ ^3 run function rlk:mboss/hz/line {len:28,w:6,tell:24,dmg:50}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_fg_p3g
execute at @s rotated as @s rotated ~90 0 positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/tele/mline {id:1,len:58,w:6,back:-30,tell:24,el:5,hold:133}
execute at @s rotated as @s rotated ~ 0 positioned ~ ~4.5 ~ run function rlk:mboss/fieldgen/fx/snd/pods_drop
