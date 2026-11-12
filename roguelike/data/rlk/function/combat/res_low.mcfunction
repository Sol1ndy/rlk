scoreboard players set #resM tmp 100
scoreboard players operation #resM tmp -= #resR tmp
scoreboard players operation #dmg tmp *= #resM tmp
scoreboard players operation #dmg tmp /= #100 tmp
