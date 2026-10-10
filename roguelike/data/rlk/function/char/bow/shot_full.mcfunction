scoreboard players operation #coef tmp = #bowFull tmp
function rlk:char/bow/calc
scoreboard players operation #aEl tmp = #charElem tmp
scoreboard players set #aKind tmp 3
execute unless score #k232 snd matches 1 run function rlk:snd/f259
