# Test 99: hold / release the AI (a running pattern finishes).
execute if score #lock hr matches 1 run return run scoreboard players set #lock hr 0
scoreboard players set #lock hr 1
