data modify storage rlk:pf id set from storage rlk:pinv q[0]
# 강화 단계가 바뀐 아이템도 다시 만든다(이름의 별)
scoreboard players set #enh tmp 0
function rlk:items/enh_get with storage rlk:pf
execute if score #enh tmp matches 4.. run scoreboard players set #enh tmp 3
execute store result storage rlk:pf e int 1 run scoreboard players get #enh tmp
execute store result storage rlk:pf sl int 1 run scoreboard players get #si tmp
data remove storage rlk:pf base
data modify storage rlk:pf ver set from storage rlk:items ver
function rlk:player/inv/place_fetch with storage rlk:pf
scoreboard players add #si tmp 1
data remove storage rlk:pinv q[0]
function rlk:player/inv/place_items_loop
