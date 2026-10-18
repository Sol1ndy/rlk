# 달빛 고치 removed -> 달빛 축복 받음: CRIT +15 %, DMG +50 % until the next 달빛 고치 or the fight's end.
# The gold fx runs 20 t on the player (coc/cure_fx).
scoreboard players set #bfCoc mb 0
scoreboard players set #bfBuff mb 1
scoreboard players set #bfDmgPct mb 150
scoreboard players set #mbCritAdd mb 15
scoreboard players set #mbHealPct mb 100
scoreboard players set #bfCureT mb 1
playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.8 1.6 0.27
playsound minecraft:entity.player.levelup hostile @a[tag=player] ~ ~ ~ 0.4 1.4 0.13
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 1 1.4 0.33
function rlk:mboss/butterfly/hud/refresh
