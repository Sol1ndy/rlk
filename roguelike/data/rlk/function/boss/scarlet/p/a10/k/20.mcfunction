# A10 pattern tick 20
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] run function rlk:mboss/mv/glide {t:2}
execute at @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] positioned ~ 203 ~ run function rlk:boss/scarlet/fx/p/claw_streaks {r:15}
execute at @s run function rlk:boss/scarlet/fx/snd/a10_dive
execute at @s positioned ~ ~1.0 ~ facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run function rlk:boss/scarlet/fx/p/qi_line {len:60}
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:15}
