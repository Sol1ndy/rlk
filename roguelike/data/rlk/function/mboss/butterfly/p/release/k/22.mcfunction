# release clock 22
function rlk:mboss/butterfly/rig_stub/face/track
# whirl: slash streaks round her, the pulsing lime 4-point star flare at her right side
execute rotated as @s rotated ~ 0 positioned ^0 ^3.24 ^0.23 run function rlk:mboss/butterfly/fx/p/rel_slashes
execute rotated as @s rotated ~ 0 positioned ^0 ^3.24 ^0.23 positioned ^-1.2 ^ ^ run function rlk:mboss/butterfly/fx/p/rel_flare
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.4 1.6 0.13
