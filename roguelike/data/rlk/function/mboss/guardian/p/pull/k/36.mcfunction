# pull tick 36 (@s = body, at the body).
# Swing clip (46 t): wind-up 0-5, hold 5-14, swing 1 at clip 15 (= 51), swing 2 at clip 28 (= 64); hazards r 6.8, tell 15.
function rlk:mboss/guardian/rig/play/swing
scoreboard players set #hzSfx mb 0
scoreboard players set #hzAct mb 3
scoreboard players set #hzVis mb 41
execute positioned ~ 201 ~ rotated as @s rotated ~ 0 run function rlk:mboss/hz/sector {r:68,a:180,tell:15,dmg:120}
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.4 0.8 0.13
