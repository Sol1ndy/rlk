# Hook bars (@s = body, every tick in intro / fight while the bars are on): the under bar = the shield (electro, 5)
# or the down timer (gold, 200); nothing while the module HUD is off (#hud 0: CS1).
execute if score #hud hr matches 0 run return 0
execute if score #shb hr matches 1 run return run function rlk:boss/scarlet/hud/bar_shield
execute if score #ph hr matches 6 if score #kip hr matches 0 run function rlk:boss/scarlet/hud/bar_down
