# walls stand y 201..210 (every zone's floor is y 200): the brain's feet stay at or below wall top - 3 (its top 1.6 b higher)
scoreboard players operation @s cmAX = #bx0 tmp
scoreboard players add @s cmAX 60
scoreboard players operation @s cmVx = #bx1 tmp
scoreboard players remove @s cmVx 60
scoreboard players operation @s cmAZ = #bz0 tmp
scoreboard players add @s cmAZ 60
scoreboard players operation @s cmVz = #bz1 tmp
scoreboard players remove @s cmVz 60
scoreboard players set #bTop tmp 20700
scoreboard players operation @s cmVy < #bTop tmp
