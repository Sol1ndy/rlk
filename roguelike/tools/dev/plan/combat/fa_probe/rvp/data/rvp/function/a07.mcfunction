kill @e[tag=rvpR]
kill @e[tag=rvpN]
summon minecraft:armor_stand 2.5 120 0.5 {Tags:["rvpN","rlk_body"],NoGravity:1b}
data modify storage rvp:log a07 set value {}
execute as @e[tag=rvpN] at @s run function rvp:a07_as
