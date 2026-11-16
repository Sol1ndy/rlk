# @s = a 포식성 broken: its prey (held, not yet eaten) is freed; org_die; the burst.
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_prey,distance=..4,sort=nearest,limit=1] run function rlk:boss/apep/org/pred/release
function rlk:boss/apep/om/pred/play/org_die
execute at @s positioned ~ ~1.2 ~ run function rlk:boss/apep/fx/p/org_burst
execute at @s run function rlk:boss/apep/fx/snd/org_kill
