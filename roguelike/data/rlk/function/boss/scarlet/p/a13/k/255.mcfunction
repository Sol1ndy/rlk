# A13 pattern tick 255.
execute at @s run function rlk:boss/scarlet/fx/snd/g_dive
function rlk:boss/scarlet/g/spot/over
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] positioned ~ ~1 ~ run function rlk:mboss/mv/glide {t:3}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
execute if score #pips hr matches 1.. run function rlk:boss/scarlet/fx/hud/ovl {g:"black",in:0,hold:3,out:0}
