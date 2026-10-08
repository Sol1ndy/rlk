scoreboard players operation #coef tmp = #bowFull tmp
function rlk:char/bow/calc
scoreboard players operation #aEl tmp = #charElem tmp
scoreboard players set #aKind tmp 3
playsound minecraft:entity.blaze.shoot master @a ~ ~ ~ 0.5 1.4
