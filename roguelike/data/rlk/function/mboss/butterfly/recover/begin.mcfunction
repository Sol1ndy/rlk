# Groggy over: she turns to face the player (24 t), then the crescent chain re-forms (18 t).
scoreboard players set #bfSt mb 4
scoreboard players set #bfT mb 0
function rlk:mboss/butterfly/rig_stub/play/turn_h
playsound minecraft:entity.breeze.idle_air hostile @a[tag=player] ~ ~ ~ 0.4 1.2 0.13
function rlk:mboss/butterfly/hud/refresh
