# Q pattern tick 23
kill @e[type=minecraft:item_display,tag=rlk_hr_swl]
execute if score #q_hit hr matches 1 at @s positioned ~ 204.4 ~ run function rlk:mboss/mv/glide {t:8}
execute if score #q_hit hr matches 1 at @s run function rlk:boss/scarlet/fx/snd/leap
execute if score #q_hit hr matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:20}
