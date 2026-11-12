# AP-REV (plan 7.6.4-7.6.7, 8.2): the organism runtime.
# Every organism, its models and the stage's loose entities (pending spawns, bolts, the organisms' hazards); no
# progress (cleanup, the CS, a failure strike, death, the phase jumps; idempotent, any executor). The fixed
# objects (the Heart, domes, stalks, walls: rlk_ap_om_obj) are not touched here.
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_org] run function rlk:boss/apep/om/kill
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_org] on passengers run kill @s
kill @e[type=minecraft:husk,tag=rlk_mb_ap_org]
kill @e[tag=rlk_ap_om,tag=!rlk_ap_om_obj]
kill @e[type=minecraft:marker,tag=rlk_mb_ap_ospawn]
kill @e[type=minecraft:marker,tag=rlk_mb_ap_cand]
kill @e[type=minecraft:item_display,tag=rlk_mb_ap_bolt]
kill @e[type=minecraft:marker,tag=rlk_mb_ap_ohz]
kill @e[type=minecraft:marker,tag=rlk_mb_ap_wlock]
scoreboard players set #apSlots mb 0
