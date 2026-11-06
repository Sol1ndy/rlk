# Q4 stage shot tick 20
function rlk:boss/arlecchino/core/lockp
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @s run function rlk:boss/arlecchino/fx/snd/beam_aim
function rlk:boss/arlecchino/p/q4/f/aim
