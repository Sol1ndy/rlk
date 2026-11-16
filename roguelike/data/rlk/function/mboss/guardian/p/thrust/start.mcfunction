# P1 공간 찌르기 start (@s = body, #gdPT 0). Clip thrust (79 t): glow 4, glint 19, hit1 21, rise 38,
# dive 54, hit2 46, land 65, flourish 72. Lanes (quiet, no ground telegraph): 9.3 x 2.9 b locked at
# 11 (hit 10 t later), 8.4 x 2.7 b locked at 34 (hit 12 t later); damage 100 % /
# 115 % (KB 4).
kill @e[tag=rlk_mb_gd_p1]
function rlk:mboss/guardian/rig/face/player
function rlk:mboss/guardian/rig/play/thrust
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.35 1.25 0.12
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.3 1.5 0.1
