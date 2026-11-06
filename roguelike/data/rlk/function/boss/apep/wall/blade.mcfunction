# A blade at a spot (facing outward = its face to the locked feet): only inside the walk disc and off the cradle.
execute unless entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..25] run return 0
execute if entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,distance=..5.1] run return 0
execute positioned ~ 201 ~ run function rlk:boss/apep/om/wall/spawn
scoreboard players operation @e[type=minecraft:item_display,tag=rlk_ap_om_new,limit=1] apL = #apWid mb
tag @e[type=minecraft:item_display,tag=rlk_ap_om_new] remove rlk_ap_om_new
