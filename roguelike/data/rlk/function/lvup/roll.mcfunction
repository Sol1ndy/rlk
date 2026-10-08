# 선택지 뽑기 (@s = 플레이어, at @s): #pkChoices 개. 이미 가진 아이템·서로 같은 아이템은 나오지 않는다(후보가 모자라면 더 적게 나옴)
data modify storage rlk:lvpick choices set value []
data modify storage rlk:pick picked set value []
scoreboard players set #pkChar tmp 0
scoreboard players operation #pkL tmp = #pkChoices tmp
function rlk:lvup/roll_loop
