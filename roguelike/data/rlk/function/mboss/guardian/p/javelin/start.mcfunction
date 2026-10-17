# P2 공간 투창 start (@s = body, #gdPT 0). Clip javelin (76 t): spin 0, vanish 10, glyph 11,
# beam 28, rematerialise 31, release 35, launch 36, return 58, catch 63. Lane locked at 24
# (tell 12), 1 b wide to the arena edge, 130 % over 36-37; the flying spear is visual.
kill @e[tag=rlk_mb_gd_p2]
function rlk:mboss/guardian/rig/face/player
function rlk:mboss/guardian/rig/play/javelin
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.7 0.7 0.23
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.4 1.4 0.13
