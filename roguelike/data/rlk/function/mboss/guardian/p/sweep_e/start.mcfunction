# Enchanted sweep (record complete; @s = body, spear already in the element): sweep_e clip (50 t: enchant 0,
# windup 7, active 19-27): 200 degree front arc r 5, x2.5 with the recorded element, strong knockback (K16).
function rlk:mboss/guardian/rig/face/player
function rlk:mboss/guardian/rig/play/sweep_e
scoreboard players set #hzSfx mb 2
scoreboard players set #hzKB mb 4
scoreboard players set #hzAct mb 8
scoreboard players operation #hzEl mb = #gdSwEl mb
scoreboard players operation #hzCol mb = #gdSwEl mb
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:50,a:100,tell:19,dmg:250}
