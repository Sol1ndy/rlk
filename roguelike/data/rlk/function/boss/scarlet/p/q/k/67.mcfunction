# Q pattern tick 67
execute if score #q_hit hr matches 1 at @s positioned ~ 207.0 ~ run function rlk:mboss/mv/glide {t:6}
execute if score #q_hit hr matches 1 at @s run function rlk:boss/scarlet/fx/snd/leap
execute if score #q_hit hr matches 1 at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:20}
