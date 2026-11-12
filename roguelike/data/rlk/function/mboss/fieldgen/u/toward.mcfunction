# @s = body: {d} blocks toward the player when the spot passes u/okb (no turn).
$execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ^ ^ ^$(d) if function rlk:mboss/fieldgen/u/okb run tp @s ~ ~ ~
