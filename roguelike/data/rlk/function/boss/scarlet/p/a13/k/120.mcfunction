# A13 pattern tick 120.
execute if entity @a[tag=rlk_body] at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=120},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ ~0.1 ~ positioned ^ ^ ^1.2 run function rlk:boss/scarlet/fx/p/qi_x {r:25}
execute unless entity @a[tag=rlk_body] at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=120},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ ~0.1 ~ run function rlk:boss/scarlet/fx/p/qi_x {r:25}
execute at @e[type=minecraft:marker,tag=rlk_hr_cut,scores={hr=120},limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 run function rlk:boss/scarlet/fx/snd/g_x
