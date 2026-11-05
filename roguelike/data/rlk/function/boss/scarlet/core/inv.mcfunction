# rlk_mb_inv of the body (@s = body, after the state): the core window (#inv: CS1 -> CS2 / the A8 fail, the kipup, the
# lead-ins -> CS4, the intro replay), the ghost form (rlk_hr_ghost, S4), A6 ticks 0-4; else hittable.
execute if score #inv hr matches 1.. run return run tag @s add rlk_mb_inv
execute if entity @s[tag=rlk_hr_ghost] run return run tag @s add rlk_mb_inv
execute if score #pat hr matches 5 if score #pt hr matches 0..4 run return run tag @s add rlk_mb_inv
tag @s remove rlk_mb_inv
