# STUB (AP-CORE, ap_contract 1.6): the revival stage; AP-REV replaces this file.
# Macro {v}: progress + v (clamp 10000; the stage tick starts the CS at 10000).
$scoreboard players add #apHt mb $(v)
execute if score #apHt mb matches 10001.. run scoreboard players set #apHt mb 10000
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_heart,limit=1] run playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 1 1.2 0.33
scoreboard players set #apHudQ mb 1
