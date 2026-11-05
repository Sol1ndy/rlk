# A13 pattern tick 49.
execute at @s run function rlk:boss/scarlet/fx/snd/g_leap
function rlk:boss/scarlet/g/spot/over
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] positioned ~ ~2.5 ~ run function rlk:mboss/mv/leap {t:6,h:30}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
