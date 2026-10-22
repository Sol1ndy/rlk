# @s = 플레이어
execute unless score @s invCap matches 9..18 run scoreboard players set @s invCap 9
scoreboard players operation @s invCap += #slotGain tmp
execute if score @s invCap matches 19.. run scoreboard players set @s invCap 18
scoreboard players set @s invDirty 2
tellraw @s [{"text":"▣ ","color":"#4FC3C9"},{"text":"보유 칸이 늘었습니다: ","color":"#4FC3C9"},{"score":{"name":"@s","objective":"invCap"},"color":"white"},{"text":" / 18","color":"gray"}]
