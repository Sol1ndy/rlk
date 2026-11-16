# C1 pattern tick 44
function rlk:boss/arlecchino/core/lockp
function rlk:boss/arlecchino/core/lock_short
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute at @s run function rlk:boss/arlecchino/fx/snd/dash_tell
