# 43 bgtick (#azBgTT 0 = the sphere tick): the sphere follows the anchor (0, 9, +2 in the body frame), its aura;
# a lance in flight moves one step; the volleys; the fade.
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p43s,limit=1] at @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] rotated ~ 0 run tp @s ^0 ^9 ^2
execute if score #aq43L mb matches 1.. run function rlk:boss/azhdaha/p/icicle/fly
execute if score #azBgTT mb matches 0..100 run return run function rlk:boss/azhdaha/p/icicle/bkd/0_100
execute if score #azBgTT mb matches 102..200 run return run function rlk:boss/azhdaha/p/icicle/bkd/102_200
