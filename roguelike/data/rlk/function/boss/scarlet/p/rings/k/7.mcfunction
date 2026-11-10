# RINGS pattern tick 7
function rlk:mboss/mv/turn {max:10}
execute at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
function rlk:boss/scarlet/fx/follow_on
function rlk:boss/scarlet/rig/anchor/blade_mid
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run function rlk:boss/scarlet/fx/p/glint {c:2}
function rlk:boss/scarlet/fx/follow_off
execute at @s run function rlk:boss/scarlet/fx/snd/parry_cue
