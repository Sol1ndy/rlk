# #dmg × (100 + 기만의 장막 × p)%  (@s = 플레이어)
$scoreboard players set #t1 tmp $(p)
scoreboard players operation #t1 tmp *= @s nfVeil
scoreboard players add #t1 tmp 100
scoreboard players operation #dmg tmp *= #t1 tmp
scoreboard players operation #dmg tmp /= #100 tmp
