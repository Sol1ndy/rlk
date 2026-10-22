# @s steps {d} blocks forward (decimal, e.g. {d:0.4}) when the spot is free and inside the safe disc.
$execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^$(d) if function rlk:mboss/mv/ok run tp @s ~ ~ ~
