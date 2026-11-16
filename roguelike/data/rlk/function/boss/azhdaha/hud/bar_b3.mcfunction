scoreboard players set #buSub bu 335
scoreboard players operation #buSub bu -= #azB3T mb
scoreboard players set #buSubMax bu 277
execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0
execute if score #azTail mb matches 3 run scoreboard players set #buSubCol bu 1
execute if score #azTail mb matches 4 run scoreboard players set #buSubCol bu 4
