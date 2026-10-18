# B2 화염 날개의 습격 (clip wing_barrage: swings [0, 26, 64, 89]; lead 5). Crescent i of a swing s: spawn s+2+i,
# fan-out 5 t, curved dive, lands s+14+i on its marker (50 % Pyro each, one hit per swing).
# swing 1 wind-up: she turns, one wing swept back; embers at the wing tips
function rlk:mboss/butterfly/rig_stub/face/player
execute rotated as @s rotated ~ 0 positioned ^3.13 ^5.99 ^-1.33 run particle minecraft:flame ~ ~ ~ 0.3 0.3 0.3 0.02 3 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-3.13 ^5.99 ^-1.33 run particle minecraft:flame ~ ~ ~ 0.3 0.3 0.3 0.02 3 force @a[tag=player]
playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.4 0.7 0.13
