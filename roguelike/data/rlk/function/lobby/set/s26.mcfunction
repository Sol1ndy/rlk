# 시작 아이템 개수: 지금은 1개 고정(나중에 사파이어로 해금)
data modify storage rlk:config start_picks set value 1
title @s actionbar {text:"시작 아이템 개수는 나중에 사파이어로 늘릴 수 있게 됩니다",color:"#E0B255"}
scoreboard players set @s hudHold 40
function rlk:lobby/set/labels
