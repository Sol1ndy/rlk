# A8 pattern tick 218.
execute store result storage rlk:hr core.sw.d double 0.4722 run scoreboard players get #sw_n hr
function rlk:boss/scarlet/core/sw/head with storage rlk:hr core.sw
execute at @e[tag=rlk_body,limit=1] rotated as @a[tag=player,limit=1] rotated ~150 0 positioned ^ ^ ^5.8 positioned ~ 201 ~ run function rlk:boss/scarlet/g/bolt
