# C0 the lunge (far: 20 b toward the player) (@s = the body; candidates in order, checked with mv/ok; none passes: she stays).
function rlk:mboss/mv/dist
execute if score #mbDist mb matches ..218 run return run function rlk:boss/scarlet/seq/cs1/m/lunge_near
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^20 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run function rlk:mboss/mv/glide {t:8}
