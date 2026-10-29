# A1 돌진 베기 (S3, p_melee.py): pattern tick 0 (@s = the body, at it). Clock #pt tk.
scoreboard players set #done tk 0
function rlk:mboss/mv/face
function rlk:boss/tachy/rig/play/a1_dash
function rlk:boss/tachy/rig/look/chest/red
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.5 ~ run function rlk:boss/tachy/fx/p/core_flare {c:2}
function rlk:boss/tachy/fx/snd/flare_tell
