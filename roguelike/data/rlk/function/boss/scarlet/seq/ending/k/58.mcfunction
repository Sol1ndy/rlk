# ending at #sq 58 (@s = the body).
function rlk:boss/scarlet/rig/look/blade/off
function rlk:boss/scarlet/fx/snd/clash
execute at @e[tag=rlk_body,limit=1] positioned ~ ~1.3 ~ facing entity @s feet positioned ^ ^ ^1.5 run function rlk:boss/scarlet/fx/p/clash_gold
function rlk:boss/scarlet/seq/ending/m/lock
