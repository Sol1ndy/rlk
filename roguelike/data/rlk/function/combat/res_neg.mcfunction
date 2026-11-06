# 음수 저항: × (100 - R/2) / 100
scoreboard players operation #resM tmp = #resR tmp
scoreboard players operation #resM tmp /= #2 tmp
scoreboard players set #resN tmp 100
scoreboard players operation #resN tmp -= #resM tmp
scoreboard players operation #dmg tmp *= #resN tmp
scoreboard players operation #dmg tmp /= #100 tmp
