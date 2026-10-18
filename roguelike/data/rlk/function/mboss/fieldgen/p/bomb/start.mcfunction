# C1 일점 상쇄 (clip bomb_run, then slam at 58; @s = body, at it): route locked at 0, bombs 12..54 (hits +6), slam r 5 at 75.
execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute rotated as @s rotated ~ 0 run function rlk:mboss/fieldgen/p/bomb/route
playsound minecraft:block.piston.extend hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.27
playsound minecraft:block.chain.place hostile @a[tag=player] ~ ~ ~ 0.8 0.8 0.27
