# @s = body (hidden): 0.3 b/t toward the player, kept within r 12 of the centre
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.3 run tp @s ~ ~ ~
function rlk:mboss/azhdaha/u/clamp_r {r:12}
