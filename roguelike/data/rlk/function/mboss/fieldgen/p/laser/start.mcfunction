# C3 코어 (clip laser; @s = body): two beams made at 0 (tell 24), active 133 t, counter-rotating 5 deg/t.
function rlk:mboss/grp_new
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p3a]
kill @e[type=minecraft:marker,tag=rlk_mb_fg_p3b]
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzAct mb 133
scoreboard players set #hzKB mb 2
scoreboard players set #hzSfx mb 0
scoreboard players set #hzRearm mb 10
scoreboard players set #hzY0 mb -5
scoreboard players set #hzY1 mb 20
execute rotated as @s rotated ~ 0 positioned ^ ^ ^2.8 run function rlk:mboss/hz/line {len:30,w:5,tell:24,dmg:50}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_fg_p3a
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzAct mb 133
scoreboard players set #hzKB mb 2
scoreboard players set #hzSfx mb 0
scoreboard players set #hzRearm mb 10
scoreboard players set #hzY0 mb -5
scoreboard players set #hzY1 mb 20
execute rotated as @s rotated ~180 0 positioned ^ ^ ^2.8 run function rlk:mboss/hz/line {len:30,w:5,tell:24,dmg:50}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_fg_p3b
playsound minecraft:block.piston.extend hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.27
playsound minecraft:block.chain.place hostile @a[tag=player] ~ ~ ~ 0.8 1 0.27
