scoreboard players operation #rdVfxOwner rd = @s rdVId
scoreboard players set #rdVfxExists rd 0
execute as @e[tag=rlk_rd_hazard] if score @s rdHId = #rdVfxOwner rd run scoreboard players set #rdVfxExists rd 1
execute if score #rdVfxExists rd matches 0 run return run kill @s
execute unless score @s rdWind matches 1 run return 0
scoreboard players add @s rdHAge 1
execute if score @s rdHAge matches 1 run function rlk:boss/raiden/hazard/vfx_flash_1
execute if score @s rdHAge matches 2 run function rlk:boss/raiden/hazard/vfx_flash_2
execute if score @s rdHAge matches 3 run function rlk:boss/raiden/hazard/vfx_after
execute if score @s rdHAge matches 6 run function rlk:boss/raiden/hazard/vfx_fade
execute if score @s rdHAge matches 9.. run kill @s
