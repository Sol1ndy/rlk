# 도감에서 좌클릭 (@s = 플레이어). 10 탭, 11 이전 쪽, 12 다음 쪽, 8 돌아가기, 13 아이템 = 인벤토리에 바로 추가(캐릭터는 그 캐릭터로 교체)
execute if score @s pkHK matches 8 run return run function rlk:lvup/exit
# 시작 모드: 아이템 = 고르기
execute if score @s cxMode matches 1 if score @s pkHK matches 13 run return run function rlk:codex/start_take
execute if score @s pkHK matches 13 run return run function rlk:codex/give
execute if score @s cxMode matches 1 if score @s pkHK matches 10 if score @s pkHI matches 2.. run return 0
execute if score @s pkHK matches 10 run scoreboard players operation @s cxTab = @s pkHI
execute if score @s pkHK matches 10 run scoreboard players set @s cxPage 0
execute if score @s pkHK matches 11 run scoreboard players remove @s cxPage 1
execute if score @s pkHK matches 12 run scoreboard players add @s cxPage 1
# 쪽 넘김은 처음↔끝으로 이어진다 (범위 확인은 다시 그릴 때)
execute if score @s pkHK matches 11 if score @s cxPage matches ..-1 run function rlk:codex/last_page
scoreboard players set @s pkRedraw 1
execute unless score #k72 snd matches 1 run function rlk:snd/f77
