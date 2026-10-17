# P1 공간 찌르기 start (@s = body, #gdPT 0). Clip thrust (91 t): glow 4, glint 19, hit1 28, rise 38,
# dive 54, hit2 58, land 65, flourish 72. Lanes: 8.5 x 2.4 b from 16 (tell 12),
# 7.0 x 2.2 b from 42 (tell 16); damage 100 % / 115 % (KB 4).
kill @e[tag=rlk_mb_gd_p1]
function rlk:mboss/guardian/rig/face/player
function rlk:mboss/guardian/rig/play/thrust
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.35 1.25 0.3
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.3 1.5 0.3
