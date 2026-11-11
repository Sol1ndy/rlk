# Stand-in sequence repel (S2b's seq.py has none yet): the clip, 140 t, the beats the core and the tests need.
$data modify storage rlk:hr core.sq.at set value "$(at)"
scoreboard players set #sqdone hr 0
function rlk:boss/scarlet/rig/play/repel
execute at @e[tag=rlk_body,limit=1] rotated ~ 0 positioned ~ ~1.3 ~ run function rlk:boss/scarlet/fx/p/clash_gold
execute at @e[tag=rlk_body,limit=1] rotated ~ 0 run function rlk:boss/scarlet/fx/p/light_column
execute at @e[tag=rlk_body,limit=1] run function rlk:boss/scarlet/fx/snd/deflect
function rlk:mboss/mv/face
