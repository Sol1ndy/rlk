scoreboard players operation #resM tmp = #resR tmp
scoreboard players operation #resM tmp *= #4 tmp
scoreboard players add #resM tmp 100
scoreboard players operation #dmg tmp *= #100 tmp
scoreboard players operation #dmg tmp /= #resM tmp
