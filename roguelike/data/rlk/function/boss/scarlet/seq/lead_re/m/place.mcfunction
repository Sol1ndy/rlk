# Her place 8 b from the player on her line to them (already 7-9 b away: she stays; mv/ok) (@s = the body).
function rlk:mboss/mv/dist
execute if score #mbDist mb matches 70..90 run return 0
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^0 ^ ^8 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:8}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^0 ^ ^7 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:8}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^0 ^ ^6 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:8}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^0 ^ ^9 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:8}
execute at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^0 ^ ^10 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:8}
