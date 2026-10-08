scoreboard players operation #eb tmp = #burstCost tmp
scoreboard players operation #eb tmp *= #st3 tmp
scoreboard players operation #eb tmp *= @s it_stormy_eye
scoreboard players add #eb tmp 1000
scoreboard players operation #dmg tmp *= #eb tmp
scoreboard players operation #dmg tmp /= #1000 tmp
