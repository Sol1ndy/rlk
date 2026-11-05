# A9 pattern tick 17
function rlk:boss/scarlet/rig/anchor/chest
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 0.2 0.2 0.2 0 10 force @a[tag=player]
execute at @s run playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.8 2 0.27
