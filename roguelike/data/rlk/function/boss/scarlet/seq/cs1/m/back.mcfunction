# C2 the leap back 6 b away from the player (apex 1.5 b) (@s = the body; candidates in order, checked with mv/ok; none passes: she stays).
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 positioned ^ ^ ^6 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/leap {t:16,h:15}
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 positioned ^ ^ ^4.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/leap {t:16,h:15}
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 positioned ^ ^ ^3 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/leap {t:16,h:15}
