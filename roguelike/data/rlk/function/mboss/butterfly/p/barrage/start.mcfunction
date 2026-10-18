# B2 화염 날개의 습격 (clip wing_barrage: swings [4, 24, 52, 72]; lead 0). Crescent i of a swing s: spawn s+2+i,
# fan-out 5 t, curved dive of D = (L + 1.6) / 0.7 t (7..60), lands s+2+i+5+D on its
# marker (50 % Pyro each, one hit per swing); the end once the clip is over and every crescent has landed.
# swing 1 wind-up: she turns, one wing swept back; embers at the wing tips
function rlk:mboss/butterfly/rig/face/player
execute rotated as @s rotated ~ 0 positioned ^-3.821 ^5.424 ^-0.92 run particle minecraft:flame ~ ~ ~ 0.3 0.3 0.3 0.02 3 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-1.665 ^4.814 ^3.841 run particle minecraft:flame ~ ~ ~ 0.3 0.3 0.3 0.02 3 force @a[tag=player]
playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.4 0.7 0.13
