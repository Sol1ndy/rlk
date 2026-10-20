# At the player's floor point: the body contact impact (once).
scoreboard players set #aq3X mb 1
function rlk:mboss/azhdaha/fx/p/impact/5
playsound minecraft:entity.ravager.attack hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.6 0.9 0.2
