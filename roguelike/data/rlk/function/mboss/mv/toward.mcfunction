# @s steps {d} blocks toward the player's body (no turn), same checks as step.
$execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^$(d) if function rlk:mboss/mv/ok run tp @s ~ ~ ~
