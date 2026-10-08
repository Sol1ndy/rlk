# macro: e = 각인 id. 개수(12 이상은 12로 봄)가 이번에 찾는 수(#want)와 같으면 sorted 에 담는다
$execute store result score #n tmp run scoreboard players get $(e) engN
scoreboard players operation #c eng = #n tmp
execute if score #c eng matches 13.. run scoreboard players set #c eng 12
execute unless score #c eng = #want eng run return 0
$data modify storage rlk:eng sorted append value {id:"$(e)"}
execute store result storage rlk:eng sorted[-1].n int 1 run scoreboard players get #n tmp
