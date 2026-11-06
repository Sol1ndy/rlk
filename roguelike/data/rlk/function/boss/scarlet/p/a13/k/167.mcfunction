# A13 pattern tick 167.
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rlk:boss/scarlet/g/disc/throw {kb:0}
execute at @s run function rlk:boss/scarlet/fx/snd/disc_release
execute at @s run function rlk:boss/scarlet/fx/snd/disc_fly
