# @s = body: the wing element look #bfWant (1 pyro: orange-gold with magenta rims, 7 dendro: lime/opal), a 1 t
# swap with a flash of its colour.
scoreboard players operation #bfLook mb = #bfWant mb
execute if score #bfLook mb matches 1 run function rlk:mboss/butterfly/rig_stub/look/pyro
execute if score #bfLook mb matches 7 run function rlk:mboss/butterfly/rig_stub/look/dendro
execute if score #bfLook mb matches 1 run particle minecraft:dust_color_transition{from_color:[0.98f,0.843f,0.486f],to_color:[0.776f,0.502f,0.635f],scale:1.4} ~ ~3.0 ~ 1.6 1 0.6 0 12 force @a[tag=player]
execute if score #bfLook mb matches 1 run particle minecraft:flame ~ ~3.0 ~ 1.4 0.8 0.5 0.02 8 force @a[tag=player]
execute if score #bfLook mb matches 1 rotated as @s rotated ~ 0 positioned ~ ~2.8 ~ run function rlk:mboss/butterfly/fx/p/pyro_switch
execute if score #bfLook mb matches 1 run function rlk:mboss/butterfly/fx/snd/pyro_switch
execute if score #bfLook mb matches 7 run particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:1.3} ~ ~3.0 ~ 1.6 1 0.6 0 12 force @a[tag=player]
execute if score #bfLook mb matches 7 rotated as @s rotated ~ 0 positioned ~ ~2.8 ~ run function rlk:mboss/butterfly/fx/p/dendro_switch
execute if score #bfLook mb matches 7 run function rlk:mboss/butterfly/fx/snd/dendro_switch
function rlk:mboss/butterfly/hud/refresh
