# F1 pattern tick 166
function rlk:boss/arlecchino/core/np
function rlk:boss/arlecchino/rig/look/wings/open
execute at @s positioned ~ ~1 ~ run function rlk:mboss/mv/glide {t:6}
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.4 ~ run function rlk:boss/arlecchino/fx/p/wing_burst
execute at @s run function rlk:boss/arlecchino/fx/snd/wing_burst
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run function rlk:boss/arlecchino/fx/decal/flood {r:260,t:30}
