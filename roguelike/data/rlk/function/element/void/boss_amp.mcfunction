scoreboard players operation #t tmp = @s rnEr
scoreboard players operation #t tmp /= #st2 tmp
scoreboard players add #t tmp 100
scoreboard players operation #dmg tmp *= #t tmp
scoreboard players operation #dmg tmp /= #100 tmp
