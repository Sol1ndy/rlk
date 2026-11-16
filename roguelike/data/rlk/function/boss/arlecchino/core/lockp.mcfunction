# The lock marker rlk_kn_lock (pattern-tagged by its owner's cancel through rlk_kn_p) at the player's feet on
# the floor, pulled toward the arena centre until mv/ok passes (inside the safe disc, free feet and head).
kill @e[type=minecraft:marker,tag=rlk_kn_lock]
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_kn_p","rlk_kn_lock"]}
scoreboard players set #t4 kn 0
execute as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] at @s run function rlk:boss/arlecchino/core/clamp
