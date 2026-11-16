# Bite 2 of the chain: the sector locked at the player now (the fish turns to it).
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~
function rlk:boss/apep/om/face
execute if entity @s[tag=rlk_mb_ap_pemp] at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:boss/apep/org/pred/hzb_e1
execute unless entity @s[tag=rlk_mb_ap_pemp] at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:boss/apep/org/pred/hzb_u1
