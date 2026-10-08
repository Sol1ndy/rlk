# 런 시작 아이템 고르기 (@s = 플레이어): 고를 개수를 정하고 도감 화면을 '시작 모드'로 연다(커먼·레어 탭만)
execute store result score #stPick room run data get storage rlk:config start_picks
execute if score #stPick room matches ..0 run return run function rlk:room/title_late
scoreboard players set @s cxMode 1
execute at @s run function rlk:codex/open
scoreboard players set @s cxMode 1
