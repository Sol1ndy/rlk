# @s boss at its current position. Controller hides and protects rdBlink 1..9.
execute if score @s rdBlink matches 1.. run return 0
scoreboard players set @s rdWalk 0
scoreboard players set @s rdBlink 1
scoreboard players set @s rdAnim 21
function rlk:boss/raiden/movement/depart
playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~1 ~ 0.6 1.45 0.15
