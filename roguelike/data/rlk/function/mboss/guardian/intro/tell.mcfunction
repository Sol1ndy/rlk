# Entrance telegraph (K19, >= 12 t, a deliberate deviation from the PDF's "no sign"): a ground disc where the
# spear will plant (right-front of her, clip grip ^-0.62 ^ ^0.7) and a glint high above it.
scoreboard players set #hzSfx mb 1
scoreboard players set #hzKB mb 3
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:30,tell:24,dmg:100}
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 run function rlk:fx/nv/card {kind:"star",pos:"^ ^7.4 ^",rot:"~ ~",bb:"center",roll:0,spin:90,s0:0.2,s1:1.4,move:"0f,0f,0f",life:14,fade:6}
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 run playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 1 1.8 0.3
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 run playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.4 1.9 0.3
