scoreboard players set #bOff tmp 0
scoreboard players set #bFin tmp 0
scoreboard players set @s bowF -1
scoreboard players operation #bCoef tmp = #flurryCoef tmp
scoreboard players set #bFl tmp 1
function rlk:char/bow/na_shot
scoreboard players set #bFl tmp 0
execute unless score #k228 snd matches 1 run function rlk:snd/f255
