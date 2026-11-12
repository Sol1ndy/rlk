# 뽑은 노드 #nk → cur_nodes 와 used 에 추가
data modify storage rlk:room used append value 0
execute store result storage rlk:room used[-1] int 1 run scoreboard players get #nk tmp
data modify storage rlk:room cur_nodes append value 0
execute store result storage rlk:room cur_nodes[-1] int 1 run scoreboard players get #nk tmp
