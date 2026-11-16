# Test 21: the mantle of the next phase step, 1 t left (the nova).
execute unless function rlk:boss/tachy/core/force run return 0
execute if score #ph tk matches 1 run scoreboard players set #fl tk 1
execute if score #ph tk matches 1 run scoreboard players set #flnext tk 1
execute if score #ph tk matches 4.. run scoreboard players set #fl tk 2
execute if score #ph tk matches 4.. run scoreboard players set #flnext tk 2
function rlk:boss/tachy/mantle/start
scoreboard players set #sht tk 1
