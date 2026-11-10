# Q pattern tick 43
execute if score #q_hit hr matches 1 at @s positioned ~ ~0.8 ~ facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 0.4 1.5 0.4 0 40 force @a[tag=player]
execute if score #q_hit hr matches 1 at @s run function rlk:boss/scarlet/fx/snd/g_rise
