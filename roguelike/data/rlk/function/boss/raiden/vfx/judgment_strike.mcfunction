summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_sfx","rlk_rd_sfx_new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_signature/judgment_strike_0"}},item_display:"none",brightness:{sky:15,block:15},view_range:4f,shadow_radius:0f,width:0f,height:0f,interpolation_duration:1,start_interpolation:0,transformation:{translation:[0f,0f,0f],scale:[16f,16f,16f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,1f,0f,0f]}}
scoreboard players set @e[tag=rlk_rd_sfx_new] rdSfxAge -1
scoreboard players set @e[tag=rlk_rd_sfx_new] rdSfxLife 12
scoreboard players set @e[tag=rlk_rd_sfx_new] rdSfxKind 3
scoreboard players set @e[tag=rlk_rd_sfx_new] rdSfxStyle 0
execute if entity @e[tag=rlk_rd_dome,limit=1] run scoreboard players set @e[tag=rlk_rd_sfx_new] rdSfxStyle 1
execute if entity @e[tag=rlk_rd_dome,limit=1] run data modify entity @e[tag=rlk_rd_sfx_new,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/judgment_strike_blocked_0"
tag @e[tag=rlk_rd_sfx_new] remove rlk_rd_sfx_new
kill @e[tag=rlk_rd_sfx,scores={rdSfxKind=2}]
execute as @e[tag=rlk_rd_sfx,scores={rdSfxKind=1}] run data modify entity @s item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/dome_hit"
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1.4 0.55 0.6
playsound minecraft:entity.iron_golem.attack hostile @a[tag=player] ~ ~ ~ 1.0 0.65 0.5
playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.65 0.70 0.4
