# @s = body: the wing element look #bfWant (1 pyro: orange-gold with magenta rims, 7 dendro: lime/opal), a 1 t
# swap with a flash of its colour.
scoreboard players operation #bfLook mb = #bfWant mb
execute if score #bfLook mb matches 1 run function rlk:mboss/butterfly/rig/look/pyro
execute if score #bfLook mb matches 7 run function rlk:mboss/butterfly/rig/look/dendro
function rlk:mboss/butterfly/wx/sw/fx
function rlk:mboss/butterfly/hud/refresh
