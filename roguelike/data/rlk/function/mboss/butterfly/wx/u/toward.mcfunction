# @s = body: {d} blocks toward the player (no turn), only inside the butterfly disc (wx/u/okb).
$execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^$(d) if function rlk:mboss/butterfly/wx/u/okb run tp @s ~ ~ ~
