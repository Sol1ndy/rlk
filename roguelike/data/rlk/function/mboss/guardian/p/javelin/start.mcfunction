# P2 start (@s = body): face the player, javelin clip (76 t: spin 0, vanish 10, glyph 11, beam 28,
# rematerialise 31, release 35, launch 36, return 58, catch 63; the rig spear is hidden 10-31 and 36-63).
function rlk:mboss/guardian/rig/face/player
function rlk:mboss/guardian/rig/play/javelin
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.7 0.7 0.3
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.4 1.4 0.3
