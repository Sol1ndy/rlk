# Nova tick (#pt tk 1..45).
execute if score #pt tk matches 40 run function rlk:boss/tachy/p/mantle/nova/flash
execute if score #pt tk matches 43 run function rlk:boss/tachy/p/mantle/nova/hz
execute if score #pt tk matches 44 run function rlk:boss/tachy/p/mantle/nova/blast
execute if score #pt tk matches 45.. run scoreboard players set #done tk 1
