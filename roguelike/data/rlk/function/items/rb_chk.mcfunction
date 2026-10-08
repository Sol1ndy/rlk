# cur가 상자 제외 목록에 있으면 #ex=1 (macro: cur)
$execute if data storage rlk:items {box_exclude:["$(cur)"]} run scoreboard players set #ex tmp 1
