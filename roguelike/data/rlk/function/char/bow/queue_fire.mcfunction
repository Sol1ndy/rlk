scoreboard players operation #bOff tmp = @s bowQo
scoreboard players set #bFin tmp 0
scoreboard players set @s bowQ -1
scoreboard players operation #bCoef tmp = @s bowQc
function rlk:char/bow/na_shot
playsound minecraft:entity.arrow.shoot master @a ~ ~ ~ 0.6 1.5
