# L hover (@s = body at HIGH_Y): 0.15 b/t toward the player's x / z while the floor spot below passes mv/ok.
execute at @e[tag=rlk_body,limit=1] positioned ~ 214 ~ if entity @s[distance=..0.2] run return 0
execute at @s positioned ~ 201 ~ facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.15 if function rlk:mboss/mv/ok positioned ~ 214 ~ run tp @s ~ ~ ~
