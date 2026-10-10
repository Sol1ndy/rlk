# 선택지를 누름 → 확인 창
scoreboard players operation @s pkSel = @s pkHI
scoreboard players set @s pkMode 2
scoreboard players set @s pkRedraw 1
execute unless score #k72 snd matches 1 run function rlk:snd/f77
