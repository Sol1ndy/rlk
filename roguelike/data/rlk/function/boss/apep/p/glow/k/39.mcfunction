# glow #apPT 39
function rlk:mboss/mv/stop
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run tp @s ~ 201 ~
function rlk:mboss/mv/face
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run function rlk:boss/apep/fx/p/gold_glow {r:30}
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run function rlk:boss/apep/fx/snd/p3_glow
