# 캐릭터 고르기: 도감을 캐릭터 탭으로 연다 (@s = 플레이어)
function rlk:codex/open
execute if score @s pkMode matches 6 run scoreboard players set @s cxTab 5
execute if score @s pkMode matches 6 run scoreboard players set @s pkRedraw 2
