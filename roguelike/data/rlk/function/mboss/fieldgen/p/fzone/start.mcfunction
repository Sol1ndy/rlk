# F1 감소 영역 (clip field_erupt; @s = body at the centre): events [22, 40, 52, 78, 100, 116, 146, 170, 190] (strike +15).
playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.8 1 0.27
playsound minecraft:block.chain.place hostile @a[tag=player] ~ ~ ~ 0.8 1.2 0.27
execute at @s rotated as @s run particle minecraft:dust{color:[0.98f,0.871f,0.659f],scale:1} ^3.85 ^3.8 ^ 0.1 0.1 0.1 0 2 force @a[tag=player]
execute at @s rotated as @s run particle minecraft:dust{color:[0.98f,0.871f,0.659f],scale:1} ^-3.85 ^3.8 ^ 0.1 0.1 0.1 0 2 force @a[tag=player]
