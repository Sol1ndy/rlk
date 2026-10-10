# 교체 취소 → 다시 바꿀 아이템 고르기
scoreboard players set @s pkMode 3
scoreboard players set @s pkRedraw 1
execute unless score #k109 snd matches 1 run function rlk:snd/f116
