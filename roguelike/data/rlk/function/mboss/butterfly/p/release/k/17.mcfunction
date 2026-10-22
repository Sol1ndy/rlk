# release clock 17
function rlk:mboss/butterfly/rig/face/track
# whirl: slash streaks round her, the pulsing lime 4-point star flare at her right side
execute rotated as @s rotated ~ 0 positioned ^-0.43 ^4.905 ^0.233 run function rlk:mboss/butterfly/fx/p/rel_slashes
execute rotated as @s rotated ~ 0 positioned ^-0.43 ^4.905 ^0.233 positioned ^-1.2 ^ ^ run function rlk:mboss/butterfly/fx/p/rel_flare
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.4 1.6 0.13
