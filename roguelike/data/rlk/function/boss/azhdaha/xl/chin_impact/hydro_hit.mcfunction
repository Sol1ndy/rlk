# The geyser erupts (the hit tick): column, stream ring, sounds.
kill @e[type=minecraft:marker,tag=rlk_mb_az_xlgk]
function rlk:boss/azhdaha/fx/p/geyser
function rlk:boss/azhdaha/fx/p/dust_ring/2 {r:30}
playsound minecraft:entity.player.splash.high_speed hostile @a[tag=player] ~ ~ ~ 1 0.8 0.33
playsound minecraft:block.bubble_column.upwards_inside hostile @a[tag=player] ~ ~ ~ 1 1 0.33
