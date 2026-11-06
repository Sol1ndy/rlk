# One walk leg: 1.2 b toward the player over 8 t while she is more than 7 b away (@s = the body; candidates in order, checked with mv/ok; none passes: she stays).
execute if score #mbDist mb matches ..70 run return 0
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^1.2 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:8}
