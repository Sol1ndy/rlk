# Q4 the aim line (@s = body, every 2 t of the aim): from the chest anchor toward the player's eyes, pitch counts.
kill @e[type=minecraft:marker,tag=rlk_kn_q4c]
function rlk:boss/arlecchino/p/q4/f/chest
execute at @e[tag=rlk_body,limit=1] anchored eyes positioned ^ ^ ^ run function rlk:boss/arlecchino/p/q4/f/dist3
execute store result storage rlk:kn p2.aim.len int 1 run scoreboard players get #q4_r kn
execute at @e[type=minecraft:marker,tag=rlk_kn_q4c,limit=1] facing entity @e[tag=rlk_body,limit=1] eyes run function rlk:boss/arlecchino/fx/p/aim_line with storage rlk:kn p2.aim
