scoreboard players add @s rdSfxAge 1
execute if score @s rdSfxAge >= @s rdSfxLife run return run kill @s
execute if score @s rdSfxKind matches 1 unless entity @e[tag=rlk_rd_dome,limit=1] run return run kill @s
execute if score @s rdSfxKind matches 2 unless entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime=..119},limit=1] run return run kill @s
execute if score @s rdSfxKind matches 4 unless entity @e[tag=rlk_raiden,scores={rdPhase=1},limit=1] run return run kill @s
execute if score @s rdSfxKind matches 2 if score @s rdSfxAge matches 35 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/judgment_charge_0"
execute if score @s rdSfxKind matches 2 if score @s rdSfxAge matches 75 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/judgment_charge_1"
execute if score @s rdSfxKind matches 2 if score @s rdSfxAge matches 105 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/judgment_charge_2"
execute if score @s rdSfxKind matches 3 if score @s rdSfxAge matches 1 run execute if score @s rdSfxStyle matches 0 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/judgment_strike_1"
execute if score @s rdSfxKind matches 3 if score @s rdSfxAge matches 2 run execute if score @s rdSfxStyle matches 0 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/judgment_strike_2"
execute if score @s rdSfxKind matches 3 if score @s rdSfxAge matches 4 run execute if score @s rdSfxStyle matches 0 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/judgment_after"
execute if score @s rdSfxKind matches 3 if score @s rdSfxAge matches 1 run execute if score @s rdSfxStyle matches 1 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/judgment_strike_blocked_1"
execute if score @s rdSfxKind matches 3 if score @s rdSfxAge matches 2 run execute if score @s rdSfxStyle matches 1 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/judgment_strike_blocked_2"
execute if score @s rdSfxKind matches 3 if score @s rdSfxAge matches 4 run execute if score @s rdSfxStyle matches 1 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/judgment_after_blocked"
execute if score @s rdSfxKind matches 1 if entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime=120},limit=1] run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/dome_hit"
execute if score @s rdSfxKind matches 1 if entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime=125},limit=1] run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/dome_crack_1"
execute if score @s rdSfxKind matches 1 if entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime=134},limit=1] run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/dome_crack_2"
execute if score @s rdSfxKind matches 1 if entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime=145},limit=1] run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/dome_crack_3"
execute if score @s rdSfxKind matches 1 if entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime=149},limit=1] run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/dome_fracture_0"
execute if score @s rdSfxKind matches 1 if entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime=155},limit=1] run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/dome_fracture_1"
execute if score @s rdSfxKind matches 1 if entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime=161},limit=1] run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/dome_fracture_2"
execute if score @s rdSfxKind matches 1 if entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime=167},limit=1] run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/dome_fracture_3"
execute if score @s rdSfxKind matches 1 if entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime=171},limit=1] run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/dome_shatter_0"
execute if score @s rdSfxKind matches 1 if entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime=173},limit=1] run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/dome_shatter_1"
execute if score @s rdSfxKind matches 1 if entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime=175},limit=1] run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/dome_shatter_2"
execute if score @s rdSfxKind matches 1 if entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime=125},limit=1] run playsound minecraft:block.respawn_anchor.deplete hostile @a[tag=player] ~ ~ ~ 0.3 1.3 .2
execute if score @s rdSfxKind matches 1 if entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime=145},limit=1] run playsound minecraft:entity.iron_golem.damage hostile @a[tag=player] ~ ~ ~ 0.35 1.2 .2
execute if score @s rdSfxKind matches 1 if entity @e[tag=rlk_raiden,scores={rdPat=15,rdTime=171},limit=1] run playsound minecraft:block.beacon.deactivate hostile @a[tag=player] ~ ~ ~ 0.55 1.1 .2
execute if score @s rdSfxKind matches 5 if score @s rdSfxAge matches 0 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/blink_scatter_3"
execute if score @s rdSfxKind matches 5 if score @s rdSfxAge matches 2 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/blink_scatter_2"
execute if score @s rdSfxKind matches 5 if score @s rdSfxAge matches 4 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/blink_scatter_1"
execute if score @s rdSfxKind matches 5 if score @s rdSfxAge matches 6 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/blink_scatter_0"
execute if score @s rdSfxKind matches 5 if score @s rdSfxAge matches 8 run data merge entity @s {interpolation_duration:1,start_interpolation:0,transformation:{scale:[0.1f,16f,0.1f],translation:[0f,0f,0f]}}
execute if score @s rdSfxKind matches 6 if score @s rdSfxAge matches 0 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/blink_scatter_0"
execute if score @s rdSfxKind matches 6 if score @s rdSfxAge matches 1 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/blink_scatter_1"
execute if score @s rdSfxKind matches 6 if score @s rdSfxAge matches 3 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/blink_scatter_2"
execute if score @s rdSfxKind matches 6 if score @s rdSfxAge matches 5 run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/blink_scatter_3"
execute if score @s rdSfxKind matches 7 if score @s rdSfxAge matches 1 run data merge entity @s {interpolation_duration:2,start_interpolation:0,transformation:{scale:[22f,19f,22f],translation:[0f,0.15f,0f]}}
execute if score @s rdSfxKind matches 7 if score @s rdSfxAge matches 5 run data merge entity @s {interpolation_duration:4,start_interpolation:0,transformation:{scale:[27f,20f,27f],translation:[0f,-0.4f,0f]}}
execute if score @s rdSfxKind matches 7 if score @s rdSfxAge matches 10 run data merge entity @s {interpolation_duration:4,start_interpolation:0,transformation:{scale:[30f,16f,30f],translation:[0f,-3f,0f]}}
