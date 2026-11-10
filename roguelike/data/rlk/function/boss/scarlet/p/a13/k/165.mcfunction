# A13 pattern tick 165.
function rlk:boss/scarlet/g/cut/lock {s:172}
function rlk:boss/scarlet/fx/follow_on
function rlk:boss/scarlet/rig/anchor/blade_mid
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/glint {c:2}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
function rlk:mboss/mv/face
function rlk:boss/scarlet/g/spot/side
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run function rlk:mboss/mv/glide {t:3}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
