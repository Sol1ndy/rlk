# A9: lock the player's spot (@s = the body). The marker rlk_hr_lock carries the pattern tags (its cancel
# kills it); core/clamp pulls it toward the arena axis until mv/ok passes there.
kill @e[type=minecraft:marker,tag=rlk_hr_lock]
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a9","rlk_hr_lock"]}
scoreboard players set #t4 hr 0
execute as @e[type=minecraft:marker,tag=rlk_hr_lock,limit=1] at @s run function rlk:boss/scarlet/core/clamp
