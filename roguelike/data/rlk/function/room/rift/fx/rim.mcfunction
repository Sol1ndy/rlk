# Rotated toward the player: the rim points k and k + 4 (k = #riftP room) get a spark each, k gets an ink puff.
execute if score #riftP room matches 0 positioned ^0 ^2.75 ^ run particle minecraft:electric_spark ~ ~ ~ 0.05 0.05 0.05 0.03 1
execute if score #riftP room matches 0 positioned ^0 ^0.15 ^ run particle minecraft:electric_spark ~ ~ ~ 0.05 0.05 0.05 0.03 1
execute if score #riftP room matches 0 positioned ^0 ^2.75 ^ run particle minecraft:squid_ink ~ ~ ~ 0.02 0.02 0.02 0.005 1
execute if score #riftP room matches 1 positioned ^0.601 ^2.369 ^ run particle minecraft:electric_spark ~ ~ ~ 0.05 0.05 0.05 0.03 1
execute if score #riftP room matches 1 positioned ^-0.601 ^0.531 ^ run particle minecraft:electric_spark ~ ~ ~ 0.05 0.05 0.05 0.03 1
execute if score #riftP room matches 1 positioned ^0.553 ^2.369 ^ run particle minecraft:squid_ink ~ ~ ~ 0.02 0.02 0.02 0.005 1
execute if score #riftP room matches 2 positioned ^0.85 ^1.45 ^ run particle minecraft:electric_spark ~ ~ ~ 0.05 0.05 0.05 0.03 1
execute if score #riftP room matches 2 positioned ^-0.85 ^1.45 ^ run particle minecraft:electric_spark ~ ~ ~ 0.05 0.05 0.05 0.03 1
execute if score #riftP room matches 2 positioned ^0.782 ^1.45 ^ run particle minecraft:squid_ink ~ ~ ~ 0.02 0.02 0.02 0.005 1
execute if score #riftP room matches 3 positioned ^0.601 ^0.531 ^ run particle minecraft:electric_spark ~ ~ ~ 0.05 0.05 0.05 0.03 1
execute if score #riftP room matches 3 positioned ^-0.601 ^2.369 ^ run particle minecraft:electric_spark ~ ~ ~ 0.05 0.05 0.05 0.03 1
execute if score #riftP room matches 3 positioned ^0.553 ^0.531 ^ run particle minecraft:squid_ink ~ ~ ~ 0.02 0.02 0.02 0.005 1
