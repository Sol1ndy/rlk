# Stand-in intro (E6-E9): a 12-t glide leg of 1.8 b toward the player while farther than 7 b (mv/ok-checked).
execute at @s if entity @e[tag=rlk_body,limit=1,distance=..7] run return 0
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^1.8 positioned ~ 201 ~ if function rlk:mboss/mv/ok run function rlk:mboss/mv/glide {t:12}
