# sweep clock 6
function rlk:mboss/butterfly/rig_stub/face/track
execute rotated as @s rotated ~ 0 positioned ^3.13 ^5.99 ^-1.33 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.01 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-3.13 ^5.99 ^-1.33 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.01 2 force @a[tag=player]
# downstroke 1
execute rotated as @s rotated ~ 0 run particle minecraft:small_flame ^ ^2.5 ^ 3 0.3 0.6 0.01 6 force @a[tag=player]
playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~ ~ 0.8 1.2 0.27
