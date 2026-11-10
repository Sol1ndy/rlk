# One step of the retreat: 0.12 b away from the player while nearer than 10.0 b (mv/ok) (@s = the body).
function rlk:mboss/mv/dist
execute if score #mbDist mb matches 100.. run return 0
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 positioned ^ ^ ^0.12 positioned ~ 201 ~ if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~
