# 묶음을 3~6번 칸에 하나씩 (남은 묶음은 gq 에 남아 7번 칸으로)
execute unless data storage rlk:eng gq[0] run return 0
execute if score #slot eng matches 7.. run return 0
function rlk:engravings/info_gitem
scoreboard players add #slot eng 1
data remove storage rlk:eng gq[0]
function rlk:engravings/info_gitem_loop
