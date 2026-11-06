# E2 to 3 b before the player (@s = the body; candidates in order, checked with mv/ok; none passes: she stays).
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^0 ^ ^3 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:8}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^0 ^ ^3.6 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:8}
