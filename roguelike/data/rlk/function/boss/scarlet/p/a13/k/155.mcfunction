# A13 pattern tick 155.
function rlk:boss/scarlet/rig/look/blade/off
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
function rlk:boss/scarlet/g/disc/throw {kb:0}
execute at @s run function rlk:boss/scarlet/fx/snd/disc_release
execute at @s run function rlk:boss/scarlet/fx/snd/disc_fly
function rlk:boss/scarlet/rig/play/a7_throw
function rlk:mboss/mv/face
