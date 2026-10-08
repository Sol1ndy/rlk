# 바꿀 인벤 아이템을 누름 → 한 번 더 묻는다(모드 5)
scoreboard players operation @s pkSwap = @s pkHI
scoreboard players set @s pkMode 5
scoreboard players set @s pkRedraw 1
playsound minecraft:ui.button.click master @s ~ ~ ~ 0.5 1.2
