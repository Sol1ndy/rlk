# 선택지를 누름 → 확인 창
scoreboard players operation @s pkSel = @s pkHI
scoreboard players set @s pkMode 2
scoreboard players set @s pkRedraw 1
playsound minecraft:ui.button.click master @s ~ ~ ~ 0.5 1.2
