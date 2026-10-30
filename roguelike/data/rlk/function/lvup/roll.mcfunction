# 선택지 뽑기 (@s = 플레이어, at @s): #pkChoices 개. 이미 가진 아이템·서로 같은 아이템은 나오지 않는다(후보가 모자라면 더 적게 나옴)
data modify storage rlk:lvpick choices set value []
data modify storage rlk:pick picked set value []
scoreboard players set #pkChar tmp 0
# 중간보스 보상(pkMb)으로 여는 묶음은 아이템만: 캐릭터 카드 없음. 묶음 표시(mbSet)는 다시 굴려도(리롤) 유지
data remove storage rlk:lvpick mbSet
execute if score @s pkMb matches 1.. run data modify storage rlk:lvpick mbSet set value 1b
execute if data storage rlk:lvpick {mbSet:1b} run scoreboard players set #pkChar tmp 1
scoreboard players operation #pkL tmp = #pkChoices tmp
function rlk:lvup/roll_loop
