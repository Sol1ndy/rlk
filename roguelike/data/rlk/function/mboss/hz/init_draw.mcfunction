# Particle drawing parameters in the marker's data (read with "with storage rlk:mboss hzp"):
# k/k0 = outer/inner circle bucket (0.5 b, max 30 b), kr = ray bucket (max 45 b), kw = bar bucket.
scoreboard players operation #kraw mb = @s mbHzR
scoreboard players add #kraw mb 250
scoreboard players operation #kraw mb /= #c500 mb
scoreboard players operation #k0raw mb = @s mbHzR0
scoreboard players add #k0raw mb 250
scoreboard players operation #k0raw mb /= #c500 mb
scoreboard players operation #k mb = #kraw mb
execute if score #k mb matches ..0 run scoreboard players set #k mb 1
execute if score #k mb matches 61.. run scoreboard players set #k mb 60
execute store result entity @s data.k int 1 run scoreboard players get #k mb
scoreboard players operation #k0 mb = #k0raw mb
execute if score #k0 mb matches ..0 run scoreboard players set #k0 mb 1
execute if score #k0 mb matches 61.. run scoreboard players set #k0 mb 60
execute store result entity @s data.k0 int 1 run scoreboard players get #k0 mb
scoreboard players operation #kr mb = #kraw mb
execute unless score @s mbHzK matches 4 run scoreboard players operation #kr mb -= #k0raw mb
execute if score @s mbHzK matches 4 run scoreboard players operation #kr mb += #k0raw mb
execute if score #kr mb matches ..0 run scoreboard players set #kr mb 1
execute if score #kr mb matches 91.. run scoreboard players set #kr mb 90
execute store result entity @s data.kr int 1 run scoreboard players get #kr mb
execute store result entity @s data.a int 1 run scoreboard players get @s mbHzAng
execute store result entity @s data.r0b double 0.001 run scoreboard players get @s mbHzR0
execute store result entity @s data.nb double -0.001 run scoreboard players get @s mbHzR0
execute store result entity @s data.lenb double 0.001 run scoreboard players get @s mbHzR
execute store result entity @s data.hw double 0.001 run scoreboard players get @s mbHzC
execute store result entity @s data.nhw double -0.001 run scoreboard players get @s mbHzC
scoreboard players operation #kw mb = @s mbHzC
scoreboard players operation #kw mb /= #c500 mb
scoreboard players operation #kw mb *= #c2 mb
execute if score #kw mb matches ..0 run scoreboard players set #kw mb 1
execute if score #kw mb matches 41.. run scoreboard players set #kw mb 40
execute store result entity @s data.kw int 1 run scoreboard players get #kw mb
data modify entity @s data.sc set value "1.0"
execute if score @s mbHzCol matches 0 run data modify entity @s data.col set from storage rlk:mboss hzc[0]
execute if score @s mbHzCol matches 1 run data modify entity @s data.col set from storage rlk:mboss hzc[1]
execute if score @s mbHzCol matches 2 run data modify entity @s data.col set from storage rlk:mboss hzc[2]
execute if score @s mbHzCol matches 3 run data modify entity @s data.col set from storage rlk:mboss hzc[3]
execute if score @s mbHzCol matches 4 run data modify entity @s data.col set from storage rlk:mboss hzc[4]
execute if score @s mbHzCol matches 5 run data modify entity @s data.col set from storage rlk:mboss hzc[5]
execute if score @s mbHzCol matches 6 run data modify entity @s data.col set from storage rlk:mboss hzc[6]
execute if score @s mbHzCol matches 7 run data modify entity @s data.col set from storage rlk:mboss hzc[7]
execute if score @s mbHzCol matches 8 run data modify entity @s data.col set from storage rlk:mboss hzc[8]
execute if score @s mbHzCol matches 9 run data modify entity @s data.col set from storage rlk:mboss hzc[9]
execute if score @s mbHzCol matches 10 run data modify entity @s data.col set from storage rlk:mboss hzc[10]
