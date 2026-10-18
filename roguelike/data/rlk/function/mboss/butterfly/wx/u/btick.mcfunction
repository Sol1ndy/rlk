# @s = body, at it, every module tick in butterfly form (the core tick): the body leash at r 16.5 (plan Q9: 0.3 b/t back toward the axis; her own glides stay inside), then S6 section 3:
# while the wings are Pyro, every 6 t a small flame and a magenta-pink spark at each forewing tip.
execute positioned ~ 201 ~ unless entity @e[tag=rlk_mb_arena,distance=..16.5,limit=1] facing entity @e[tag=rlk_mb_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.3 run tp @s ~ ~ ~
execute unless score #bfLook mb matches 1 run return 0
scoreboard players operation #bfM mb = #bfClk mb
scoreboard players operation #bfM mb %= #bfK6 mb
execute if score #bfM mb matches 0 run function rlk:mboss/butterfly/wx/sw/embers
