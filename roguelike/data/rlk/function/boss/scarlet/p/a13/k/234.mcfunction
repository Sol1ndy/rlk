# A13 pattern tick 234.
function rlk:boss/scarlet/rig/look/blade/pink
function rlk:boss/scarlet/rig/anchor/blade_tip
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] rotated as @s run particle minecraft:dust{color:[0.88,0.25,0.62],scale:1.2} ~ ~ ~ 0.1 0.1 0.1 0 8 force @a[tag=player]
execute at @s run playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.6 1.9 0.2
