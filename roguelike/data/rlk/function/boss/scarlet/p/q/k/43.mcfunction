# Q pattern tick 43
execute if score #q_hit hr matches 1 at @s positioned ~ ~0.8 ~ facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run function rlk:boss/scarlet/fx/p/qi_beam {len:140}
execute if score #q_hit hr matches 1 at @s run function rlk:boss/scarlet/fx/snd/g_rise
