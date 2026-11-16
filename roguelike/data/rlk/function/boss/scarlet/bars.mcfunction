# Hook bars (@s = body, every tick in intro / fight while the bars are on): the under bar = the 5-segment gauge
# (electro) from control to the ending; nothing while the module HUD is off (#hud 0: CS1). The HP bar fills over the
# first 30 t of the fight (mboss/bars_ramp: its intro ramp, here at control, the bars being off in CS0).
execute if score #mbSt mb matches 1 if score #mbT mb matches ..29 run function rlk:mboss/bars_ramp
execute if score #hud hr matches 0 run return 0
execute if score #mbSt mb matches 1 run function rlk:boss/scarlet/hud/bar_shield
