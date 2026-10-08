# 좌클릭 (@s = 플레이어, at @s). 조준 중인 요소(pkHK 종류, pkHI 번호)에 따라
# 한 번의 클릭이 두 경로(발전과제 → 다음 틱에 인터랙션 폴링)로 잇따라 들어오므로, 처리한 뒤 몇 틱은 무시한다
execute if score @s pkCd matches 1.. run return 0
scoreboard players set @s pkCd 4
execute if score @s pkRedraw matches 1.. run return 0
execute if score @s pkHK matches 0 run return 0
execute if score @s pkMode matches 4 run return run function rlk:invd/click
execute if score @s pkMode matches 6 run return run function rlk:codex/click
execute if score @s pkHK matches 1 run return run function rlk:lvup/act/choose
execute if score @s pkHK matches 3 run return run function rlk:lvup/act/reroll
execute if score @s pkHK matches 4 run return run function rlk:lvup/act/skip
execute if score @s pkMode matches 5 if score @s pkHK matches 5 run return run function rlk:lvup/act/swap_do
execute if score @s pkMode matches 5 if score @s pkHK matches 6 run return run function rlk:lvup/act/swap_back
execute if score @s pkHK matches 5 run return run function rlk:lvup/act/confirm
execute if score @s pkHK matches 6 run return run function rlk:lvup/act/cancel
execute if score @s pkHK matches 2 if score @s pkMode matches 3 run return run function rlk:lvup/act/swap
