# Timed cards: countdown (not on their summon tick), kill at 0, strike frames by remaining life.
scoreboard players remove @e[tag=rlk_rd_fx,tag=!rlk_rd_fxnew] rdHLife 1
kill @e[tag=rlk_rd_fx,scores={rdHLife=..0}]
execute as @e[tag=rlk_rd_strike,tag=rlk_rd_fx,scores={rdHLife=9}] run data modify entity @s item.components."minecraft:custom_model_data".colors[0] set value 13154026
execute as @e[tag=rlk_rd_strike,tag=rlk_rd_fx,scores={rdHLife=8}] run data modify entity @s item.components."minecraft:custom_model_data".colors[0] set value 15590655
execute as @e[tag=rlk_rd_strike,tag=rlk_rd_fx,scores={rdHLife=7}] run function rlk:boss/raiden/hazard/fx_after
execute as @e[tag=rlk_rd_fx,scores={rdHLife=4}] run function rlk:boss/raiden/hazard/fx_fade
