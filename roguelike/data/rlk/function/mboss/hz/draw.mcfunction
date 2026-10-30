# Telegraph: outline plus a progress outline that reaches the rim when the hit lands.
data modify storage rlk:mboss hzp set from entity @s data
scoreboard players operation #p mb = @s mbHzT
scoreboard players operation #p mb *= #c1000 mb
scoreboard players operation #p mb /= @s mbHzW
execute store result score #kp mb run data get storage rlk:mboss hzp.k
scoreboard players operation #kp mb *= #p mb
scoreboard players operation #kp mb /= #c1000 mb
execute if score #kp mb matches ..0 run scoreboard players set #kp mb 1
execute store result storage rlk:mboss hzp.kp int 1 run scoreboard players get #kp mb
scoreboard players operation #hzAng mb = @s mbHzAng
execute if score @s mbHzK matches 1 run function rlk:mboss/hz/d/disc with storage rlk:mboss hzp
execute if score @s mbHzK matches 2 run function rlk:mboss/hz/d/ring with storage rlk:mboss hzp
execute if score @s mbHzK matches 3 run function rlk:mboss/hz/d/sector with storage rlk:mboss hzp
execute if score @s mbHzK matches 4 run function rlk:mboss/hz/draw_line
execute if score @s mbHzK matches 5 run function rlk:mboss/hz/d/full with storage rlk:mboss hzp
