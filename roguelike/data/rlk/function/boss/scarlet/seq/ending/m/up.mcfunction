# E10 the leap up and back (4 b off, 5 b up) (@s = the body; candidates in order, checked with mv/ok; none passes: she stays).
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^4 positioned ~ 206 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:8}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^3 positioned ~ 206 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:8}
