# Test 31: the dark look on / off (crimson).
execute if score #lk hr matches 3 run scoreboard players set #hrLook hr 2
execute if score #lk hr matches 3 run return run scoreboard players set #lk hr 2
scoreboard players set #hrLook hr 3
scoreboard players set #lk hr 3
