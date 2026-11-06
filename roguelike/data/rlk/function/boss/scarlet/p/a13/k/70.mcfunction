# A13 pattern tick 70.
function rlk:boss/scarlet/g/cut/aim {s:80}
execute at @e[tag=rlk_body,limit=1] rotated as @a[tag=player,limit=1] rotated ~-60 0 positioned ^ ^ ^3.6 positioned ~ 201 ~ run function rlk:boss/scarlet/g/bolt
