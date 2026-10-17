# Gold sweep (guard timeout; @s = body): sweep clip (44 t, active 19-24): 200 degree front arc, r 5 (K6).
function rlk:mboss/guardian/rig/face/player
function rlk:mboss/guardian/rig/play/sweep
playsound minecraft:item.trident.riptide_2 hostile @a[tag=player] ~ ~ ~ 0.7 0.7 0.3
scoreboard players set #hzSfx mb 2
scoreboard players set #hzKB mb 3
scoreboard players set #hzAct mb 5
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:50,a:100,tell:19,dmg:165}
