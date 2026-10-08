# 얼음 투창 (@s = 플레이어, at @s): 투창 3개(차가운 별빛 8스택이면 5개)를 0.15초 간격으로 던진다. 별빛 스택당 피해 +6.5%
scoreboard players set @s javQ 3
execute if score @s starlight matches 8.. run scoreboard players set @s javQ 5
scoreboard players operation @s javN = @s javQ
scoreboard players operation @s javBonus = @s starlight
scoreboard players operation @s javBonus *= #c65 tmp
scoreboard players set @s starlight 0
scoreboard players set @s javT 0
playsound minecraft:item.trident.thunder master @a ~ ~ ~ 0.35 1.8
playsound minecraft:block.glass.break master @a ~ ~ ~ 0.8 0.6
playsound minecraft:block.respawn_anchor.set_spawn master @a ~ ~ ~ 0.6 1.6
particle minecraft:snowflake ~ ~1.2 ~ 0.6 0.8 0.6 0.08 50
particle minecraft:dust{color:[0.62f,0.91f,0.96f],scale:1.8f} ~ ~1.2 ~ 0.7 0.9 0.7 0 20
