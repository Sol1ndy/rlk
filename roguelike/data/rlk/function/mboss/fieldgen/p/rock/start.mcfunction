# C6 파쇄 (clip tower_throw; @s = body): bursts from 55, throws from 95.
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
playsound minecraft:block.piston.extend hostile @a[tag=player] ~ ~ ~ 0.8 0.5 0.27
