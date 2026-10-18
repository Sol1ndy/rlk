# C4 바위 폭탄 (clip missiles; @s = body): launches [21, 22, 24, 25, 27, 28, 30, 31, 33, 34], lock +7, impact +20.
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.8 1.4 0.27
execute at @s rotated as @s run particle minecraft:end_rod ^3.6 ^4.6 ^ 0.1 0.1 0.1 0.02 2 force @a[tag=player]
execute at @s rotated as @s run particle minecraft:end_rod ^-3.6 ^4.6 ^ 0.1 0.1 0.1 0.02 2 force @a[tag=player]
