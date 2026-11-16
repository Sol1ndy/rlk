# 이번 선택 끝: 남은 기회가 있으면 새 선택지, 없으면 돌아간다
scoreboard players remove @s pkPending 1
# 중간보스 보상 묶음을 하나 썼음(미리 굴려 둔 레벨 업 묶음은 그대로): 이때 열린 아이템 상자 하나가 사라진다(mboss/box/spend,
# 가장 먼저 연 상자. 열린 상자가 없으면 = 그 방을 떠났으면 아무것도 지우지 않음)
execute if data storage rlk:lvpick {mbSet:1b} if score @s pkMb matches 1.. run function rlk:mboss/box/spend
execute if data storage rlk:lvpick {mbSet:1b} if score @s pkMb matches 1.. run scoreboard players remove @s pkMb 1
data remove storage rlk:lvpick mbSet
scoreboard players set @s pkSel -1
# 다음 선택의 첫 리롤은 다시 무료
scoreboard players set @s pkRr 0
data modify storage rlk:lvpick choices set value []
execute unless score @s pkPending matches 1.. run return run function rlk:lvup/exit
scoreboard players set @s pkMode 1
# 방금 얻은 아이템이 인벤 목록에 반영된 뒤에 새 선택지를 뽑고 다시 그린다 (뽑기는 lvup/ui/draw 에서: 선택지가 비어 있으면 뽑음)
scoreboard players set @s pkRedraw 4
