execute if score @s cmT matches 1.. run return run function rlk:cm/pj/ic_hang
scoreboard players remove @s cmT 1
execute if score @s cmT matches ..-40 run return run kill @s
scoreboard players add @s cmV 12
execute if score @s cmV matches 141.. run scoreboard players set @s cmV 140
scoreboard players operation #pst tmp = @s cmV
scoreboard players operation #pst tmp /= #35 tmp
execute if score #pst tmp matches ..0 run scoreboard players set #pst tmp 1
function rlk:cm/pj/ic_step
