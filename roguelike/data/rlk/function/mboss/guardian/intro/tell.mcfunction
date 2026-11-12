# Entrance tell (K19, >= 12 t): a glint high above the spot where the spear will plant (right-front of her, clip
# grip ^-0.62 ^ ^0.7), then the spear falls from 7 b (intro/fall, intro/trail). Telegraph rule (10-20): no ground
# marker (the PDF: she appears "어떤 표시도 남기지 않은 상태에서"), so the plant disc is quiet (#hzQuiet 1: no
# framework outline, no strike flash); the plant's own impact (intro/impact) shows the area.
scoreboard players set #hzSfx mb 0
scoreboard players set #hzKB mb 3
scoreboard players set #hzQuiet mb 1
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 positioned ~ 201 ~ run function rlk:mboss/hz/disc {r:36,tell:18,dmg:100}
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 run function rlk:fx/nv/card {kind:"star",pos:"^ ^7.4 ^",rot:"~ ~",bb:"center",roll:0,spin:90,s0:0.2,s1:1.4,move:"0f,0f,0f",life:14,fade:6}
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 run playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 1 1.8 0.33
execute rotated as @s rotated ~ 0 positioned ^-0.62 ^ ^0.7 run playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.4 1.9 0.13
