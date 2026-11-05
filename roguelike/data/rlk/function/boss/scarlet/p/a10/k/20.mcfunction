# A10 pattern tick 20
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run function rlk:mboss/mv/glide {t:2}
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ 203 ~ run function rlk:boss/scarlet/fx/p/claw_streaks {r:15}
execute at @s run function rlk:boss/scarlet/fx/snd/a10_dive
