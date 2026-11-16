# macro: e = 각인 id. 개수(12 이상은 12로 봄)의 묶음에 {id, n} 을 담는다(개수 0 · 없음은 빠짐)
$execute store result score #n tmp run scoreboard players get $(e) engN
scoreboard players operation #c eng = #n tmp
execute if score #c eng matches 13.. run scoreboard players set #c eng 12
execute if score #c eng matches 1.. run function rlk:engravings/info_bucket_put
