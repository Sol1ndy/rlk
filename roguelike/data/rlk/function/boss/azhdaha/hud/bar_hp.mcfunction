# The phase pool: phase 1 mhpM .. F1, phase 2 F1 .. F2, phase 3 F2 .. 0 (the floors recomputed here).
scoreboard players operation #buSub bu = @s mhpC
scoreboard players operation #buSub bu -= #mbFloor mb
scoreboard players operation #azX mb = @s mhpM
scoreboard players operation #azX mb *= #c2 mb
scoreboard players add #azX mb 2
scoreboard players set #azY mb 3
scoreboard players operation #azX mb /= #azY mb
scoreboard players operation #azZ mb = @s mhpM
scoreboard players add #azZ mb 2
scoreboard players operation #azZ mb /= #azY mb
execute if score #azPh mb matches ..1 run scoreboard players operation #buSubMax bu = @s mhpM
execute if score #azPh mb matches ..1 run scoreboard players operation #buSubMax bu -= #azX mb
execute if score #azPh mb matches 2 run scoreboard players operation #buSubMax bu = #azX mb
execute if score #azPh mb matches 2 run scoreboard players operation #buSubMax bu -= #azZ mb
execute if score #azPh mb matches 3.. run scoreboard players operation #buSubMax bu = #azZ mb
execute if score #azPh mb matches 3.. run scoreboard players operation #buSubMax bu -= #mbFloor mb
execute if score #buSubMax bu matches ..0 run scoreboard players set #buSubMax bu 1
execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0
scoreboard players set #buSubCol bu 5
execute if score #azPh mb matches 2 if score #azLeg mb matches 1 run scoreboard players set #buSubCol bu 2
execute if score #azPh mb matches 2 if score #azLeg mb matches 2 run scoreboard players set #buSubCol bu 3
execute if score #azPh mb matches 3.. if score #azTail mb matches 3 run scoreboard players set #buSubCol bu 1
execute if score #azPh mb matches 3.. if score #azTail mb matches 4 run scoreboard players set #buSubCol bu 4
