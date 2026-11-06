# @s = body: {d} blocks away from the player (no turn), only inside the butterfly disc.
$execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 positioned ^ ^ ^$(d) if function rlk:mboss/butterfly/wx/u/okb run tp @s ~ ~ ~
