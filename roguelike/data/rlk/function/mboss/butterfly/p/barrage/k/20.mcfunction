# barrage clock 20
# swing 2 wind-up: she turns, one wing swept back; embers at the wing tips
function rlk:mboss/butterfly/rig/face/player
execute rotated as @s rotated ~ 0 positioned ^1.068 ^5.188 ^3.841 run particle minecraft:flame ~ ~ ~ 0.3 0.3 0.3 0.02 3 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^2.98 ^6.355 ^-0.92 run particle minecraft:flame ~ ~ ~ 0.3 0.3 0.3 0.02 3 force @a[tag=player]
playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.4 0.7 0.13
