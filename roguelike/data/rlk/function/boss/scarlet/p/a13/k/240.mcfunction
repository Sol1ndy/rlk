# A13 pattern tick 240.
execute at @s rotated ~ 90 positioned ~ ~0.8 ~ run function rlk:boss/scarlet/fx/p/qi_line {len:40}
execute at @e[tag=rlk_body,limit=1] rotated as @a[tag=player,limit=1] rotated ~150 0 positioned ^ ^ ^5.8 positioned ~ 201 ~ run function rlk:boss/scarlet/g/bolt
