# P2 공간 투창 start (@s = body, #gdPT 0). Clip javelin (67 t): spin 0, vanish 9, glyph 10,
# beam 20, rematerialise 22, release 26, launch 27, return 49, catch 54. Lane locked at 17
# (tell 10), 1.2 b wide to the arena edge, 130 % over 27-28; the flying spear is visual.
kill @e[tag=rlk_mb_gd_p2]
function rlk:mboss/guardian/rig/face/player
function rlk:mboss/guardian/rig/play/javelin
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.7 0.7 0.23
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.4 1.4 0.13
