# R5 the throw to 3.5 b before the player (@s = the body; candidates in order, checked with mv/ok; none passes: she stays).
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^ ^3.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/leap {t:15,h:25}
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^ ^2.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/leap {t:15,h:25}
execute at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^ ^1.5 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/leap {t:15,h:25}
