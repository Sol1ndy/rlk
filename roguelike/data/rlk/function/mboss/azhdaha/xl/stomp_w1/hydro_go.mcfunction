# Launch: 8 blades radially (blade 0 toward the player) from r 2, 0.9 b up.
execute rotated ~0 0 positioned ^ ^0.9 ^2 run function rlk:mboss/azhdaha/xl/u/blade
execute rotated ~45 0 positioned ^ ^0.9 ^2 run function rlk:mboss/azhdaha/xl/u/blade
execute rotated ~90 0 positioned ^ ^0.9 ^2 run function rlk:mboss/azhdaha/xl/u/blade
execute rotated ~135 0 positioned ^ ^0.9 ^2 run function rlk:mboss/azhdaha/xl/u/blade
execute rotated ~180 0 positioned ^ ^0.9 ^2 run function rlk:mboss/azhdaha/xl/u/blade
execute rotated ~225 0 positioned ^ ^0.9 ^2 run function rlk:mboss/azhdaha/xl/u/blade
execute rotated ~270 0 positioned ^ ^0.9 ^2 run function rlk:mboss/azhdaha/xl/u/blade
execute rotated ~315 0 positioned ^ ^0.9 ^2 run function rlk:mboss/azhdaha/xl/u/blade
function rlk:mboss/azhdaha/fx/p/splash
playsound minecraft:entity.player.splash.high_speed hostile @a[tag=player] ~ ~ ~ 0.9 1.2 0.3
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.6 1.5 0.2
