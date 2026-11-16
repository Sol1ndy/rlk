# @s = live hazard marker; #hzSzR / #hzSzR0 / #hzSzW mb in tenths (see hz/resize). r is clamped to 0..40 b (the
# squared bounds stay inside 32 bits).
execute if score #hzSzR mb matches ..-1 run scoreboard players set #hzSzR mb 0
execute if score #hzSzR mb matches 401.. run scoreboard players set #hzSzR mb 400
scoreboard players operation @s mbHzR = #hzSzR mb
scoreboard players operation @s mbHzR *= #c100 mb
scoreboard players operation @s mbHzR0 = #hzSzR0 mb
scoreboard players operation @s mbHzR0 *= #c100 mb
execute if score @s mbHzK matches 4 run function rlk:mboss/hz/resize_line
execute unless score @s mbHzK matches 4 run function rlk:mboss/hz/resize_rad
execute unless entity @s[tag=rlk_mb_hzq] run function rlk:mboss/hz/init_draw
