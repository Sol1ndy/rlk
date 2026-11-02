# G1 pattern tick 6
function rlk:boss/arlecchino/core/lockp
execute as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] at @s rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run tp @s ~ ~ ~ ~0 0
scoreboard players set #t kn 28
execute store result score #t2 kn run data get entity @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] Rotation[0]
scoreboard players add #t2 kn 90
data modify storage rlk:kn core.st set value {len:280,w:30,yaw:0,t:0}
function rlk:boss/arlecchino/p/g1/cross
function rlk:boss/arlecchino/p/g1/strips
