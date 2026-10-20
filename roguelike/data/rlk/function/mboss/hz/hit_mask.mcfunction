# @s = a mask hazard inside its active window (height band passed): safe when the body is near a safe marker of its group.
scoreboard players set #hzSafe mb 0
execute unless function rlk:mboss/mv/plpos run return 0
scoreboard players operation #bx mb = #mbPX mb
scoreboard players operation #bz mb = #mbPZ mb
scoreboard players operation #hzG2 mb = @s mbHzSG
scoreboard players operation #hzRI2 mb = @s mbHzRI
execute as @e[type=minecraft:marker,tag=rlk_mb_hzsafe] if score @s mbHzSG = #hzG2 mb run function rlk:mboss/hz/mask_one
execute if score #hzSafe mb matches 0 run function rlk:mboss/hz/hurt
