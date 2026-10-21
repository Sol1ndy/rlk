# STUB (AP-CORE, ap_contract 1.6): the revival stage; AP-REV replaces this file.
# Macro {v}: progress - v (clamp 0; the stage tick starts the failure strike at 0).
$scoreboard players remove #apHt mb $(v)
execute if score #apHt mb matches ..-1 run scoreboard players set #apHt mb 0
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_heart,limit=1] run playsound minecraft:block.amethyst_block.hit hostile @a[tag=player] ~ ~ ~ 0.4 0.6 0.13
scoreboard players set #apHudQ mb 1
