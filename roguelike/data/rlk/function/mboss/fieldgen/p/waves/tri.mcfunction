# Clock 135: the 3rd wave fires 3 fronts below 50 % HP (or with test 42, #fgTri 1).
scoreboard players set #fq21T mb 0
scoreboard players operation #fgX mb = @s mhpC
scoreboard players operation #fgX mb *= #c2 mb
execute if score #fgX mb < @s mhpM run scoreboard players set #fq21T mb 1
execute if score #fgTri mb matches 1 run scoreboard players set #fq21T mb 1
