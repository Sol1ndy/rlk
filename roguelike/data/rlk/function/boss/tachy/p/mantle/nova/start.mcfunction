# Nova (G2 failure; @s = body, #pt tk 0): mantle_nova 44 t, the wings swell 0-40, flash 40,
# the whole-arena hit at 44 (dash-dodgeable, 250 per mille, non-lethal, Electro).
scoreboard players set #done tk 0
function rlk:boss/tachy/rig/play/mantle_nova
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.4 ~ run function rlk:boss/tachy/fx/p/nova_swell {t:40}
execute at @s run function rlk:boss/tachy/fx/snd/nova_swell
