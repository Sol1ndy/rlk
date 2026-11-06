data modify storage rlk:mboss hzp set from entity @s data
data modify storage rlk:mboss hzp.col set from storage rlk:mboss hzc[9]
data modify storage rlk:mboss hzp.sc set value "1.5"
scoreboard players operation #hzAng mb = @s mbHzAng
execute store result score #kp mb run data get storage rlk:mboss hzp.k
scoreboard players operation #kp mb *= #c2 mb
scoreboard players operation #kp mb /= #c4 mb
execute if score #kp mb matches ..0 run scoreboard players set #kp mb 1
execute store result storage rlk:mboss hzp.kp int 1 run scoreboard players get #kp mb
scoreboard players set #p mb 500
execute if score @s mbHzK matches 1 run function rlk:mboss/hz/d/disc with storage rlk:mboss hzp
execute if score @s mbHzK matches 2 run function rlk:mboss/hz/d/ring with storage rlk:mboss hzp
execute if score @s mbHzK matches 3 run function rlk:mboss/hz/d/sector with storage rlk:mboss hzp
execute if score @s mbHzK matches 4 run function rlk:mboss/hz/draw_line
execute if score @s mbHzK matches 1..3 run particle minecraft:explosion ~ ~0.3 ~ 0.6 0.1 0.6 0 2 force @a[tag=player]
execute if score @s mbHzK matches 5 run particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1 force @a[tag=player]
