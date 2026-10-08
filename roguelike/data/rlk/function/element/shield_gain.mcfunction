# @s = 플레이어. 방어막 #amt 획득(더 클 때만 교체), 15초 유지
execute unless score @s shieldHP >= #amt tmp run scoreboard players operation @s shieldHP = #amt tmp
scoreboard players set @s shieldT 300
playsound minecraft:block.amethyst_block.chime master @s ~ ~ ~ 1 1.2
playsound minecraft:item.armor.equip_diamond master @s ~ ~ ~ 0.6 1.3
