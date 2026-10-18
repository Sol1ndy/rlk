# barrage clock 84
execute if entity @e[tag=rlk_body,distance=..5,limit=1] run function rlk:mboss/butterfly/wx/u/away {d:0.2}
# swing 4 wind-up: she turns, one wing swept back; embers at the wing tips
function rlk:mboss/butterfly/rig_stub/face/player
execute rotated as @s rotated ~ 0 positioned ^3.13 ^5.99 ^-1.33 run particle minecraft:flame ~ ~ ~ 0.3 0.3 0.3 0.02 3 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-3.13 ^5.99 ^-1.33 run particle minecraft:flame ~ ~ ~ 0.3 0.3 0.3 0.02 3 force @a[tag=player]
playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.4 0.7 0.13
