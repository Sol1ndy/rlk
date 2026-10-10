# 바꿀 인벤 아이템을 누름 → 한 번 더 묻는다(모드 5)
scoreboard players operation @s pkSwap = @s pkHI
scoreboard players set @s pkMode 5
scoreboard players set @s pkRedraw 1
execute unless score #k72 snd matches 1 run function rlk:snd/f77
