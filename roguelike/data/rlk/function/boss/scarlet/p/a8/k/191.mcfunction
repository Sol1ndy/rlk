# A8 pattern tick 191.
execute at @s run function rlk:boss/scarlet/fx/snd/g_dive
function rlk:boss/scarlet/g/spot/over
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] positioned ~ ~1 ~ run function rlk:mboss/mv/glide {t:3}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
