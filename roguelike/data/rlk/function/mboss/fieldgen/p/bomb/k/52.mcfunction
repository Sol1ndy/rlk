# bomb clock 52
execute rotated as @e[type=minecraft:marker,tag=rlk_mb_fg_p1p,limit=1] positioned ^-1.2 ^ ^ run function rlk:mboss/fieldgen/p/bomb/drop
playsound minecraft:block.dispenser.launch hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
