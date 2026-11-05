# A13 pattern tick 258.
function rlk:boss/scarlet/shield/judge
execute if score #gres hr matches 2 run function rlk:boss/scarlet/p/a13/fail
execute at @e[tag=rlk_body,limit=1] rotated as @a[tag=player,limit=1] rotated ~150 0 positioned ^ ^ ^5.8 positioned ~ 201 ~ run function rlk:boss/scarlet/g/bolt
