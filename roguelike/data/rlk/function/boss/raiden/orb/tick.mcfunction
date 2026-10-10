# As flower. HP is the existing one-Electro/four-other attack counter.
scoreboard players operation #rdOrbOwner rd = @s rdOvId
scoreboard players operation #rdOrbHP rd = @s rdObjHP
scoreboard players operation #rdOrbFrame rd = @s rdOAge
scoreboard players set #rdOrbPeriod rd 32
scoreboard players operation #rdOrbFrame rd %= #rdOrbPeriod rd
execute as @e[tag=rlk_rd_orb_gauge] if score @s rdOvId = #rdOrbOwner rd unless score @s rdObjHP = #rdOrbHP rd run function rlk:boss/raiden/orb/gauge
execute if score #rdOrbFrame rd matches 0 as @e[tag=rlk_rd_orb_body] if score @s rdOvId = #rdOrbOwner rd run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{translation:[0f,1.4500f,0f]}}
execute if score #rdOrbFrame rd matches 0 as @e[tag=rlk_rd_orb_body] if score @s rdOvId = #rdOrbOwner rd run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_orb/orb_0"
execute if score #rdOrbFrame rd matches 4 as @e[tag=rlk_rd_orb_body] if score @s rdOvId = #rdOrbOwner rd run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{translation:[0f,1.4960f,0f]}}
execute if score #rdOrbFrame rd matches 8 as @e[tag=rlk_rd_orb_body] if score @s rdOvId = #rdOrbOwner rd run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{translation:[0f,1.5150f,0f]}}
execute if score #rdOrbFrame rd matches 8 as @e[tag=rlk_rd_orb_body] if score @s rdOvId = #rdOrbOwner rd run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_orb/orb_1"
execute if score #rdOrbFrame rd matches 12 as @e[tag=rlk_rd_orb_body] if score @s rdOvId = #rdOrbOwner rd run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{translation:[0f,1.4960f,0f]}}
execute if score #rdOrbFrame rd matches 16 as @e[tag=rlk_rd_orb_body] if score @s rdOvId = #rdOrbOwner rd run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{translation:[0f,1.4500f,0f]}}
execute if score #rdOrbFrame rd matches 16 as @e[tag=rlk_rd_orb_body] if score @s rdOvId = #rdOrbOwner rd run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_orb/orb_2"
execute if score #rdOrbFrame rd matches 20 as @e[tag=rlk_rd_orb_body] if score @s rdOvId = #rdOrbOwner rd run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{translation:[0f,1.4040f,0f]}}
execute if score #rdOrbFrame rd matches 24 as @e[tag=rlk_rd_orb_body] if score @s rdOvId = #rdOrbOwner rd run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{translation:[0f,1.3850f,0f]}}
execute if score #rdOrbFrame rd matches 24 as @e[tag=rlk_rd_orb_body] if score @s rdOvId = #rdOrbOwner rd run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_orb/orb_3"
execute if score #rdOrbFrame rd matches 28 as @e[tag=rlk_rd_orb_body] if score @s rdOvId = #rdOrbOwner rd run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{translation:[0f,1.4040f,0f]}}
