# Launch: 8 blades radially (blade 0 toward the player) from r 2, 0.9 b up, two opposite
# blades per tick over 4 ticks (FIX STATE-2: eight pj/launch in one tick went over 3000 commands with the orbs up).
execute rotated ~0 0 positioned ^ ^0.9 ^2 run function rlk:boss/azhdaha/xl/u/blade
execute rotated ~180 0 positioned ^ ^0.9 ^2 run function rlk:boss/azhdaha/xl/u/blade
function rlk:boss/azhdaha/fx/p/splash
playsound minecraft:entity.player.splash.high_speed hostile @a[tag=player] ~ ~ ~ 0.9 1.2 0.3
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.6 1.5 0.2
scoreboard players set #azAftF mb 39
scoreboard players set #azAftD mb 1
function rlk:boss/azhdaha/aft/new
