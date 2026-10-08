# at = 슬롯 블록 코너. 챕터별 등급 확률(items/roll_rarity)로 등급을 굴려 아이템 1개 선택 → storage rlk:pick pid
function rlk:items/roll_rarity
function rlk:items/pick_item
# 굴린 등급에 뽑을 아이템이 없으면(다 가졌거나 후보가 없음) 낮은 등급부터 다시 찾는다. 지금 챕터에서 못 나오는 등급(#gMax 초과)은 찾지 않음
execute unless data storage rlk:pick pid run scoreboard players set #g tmp 0
execute unless data storage rlk:pick pid run function rlk:items/pick_item
execute unless data storage rlk:pick pid run scoreboard players set #g tmp 1
execute unless data storage rlk:pick pid run function rlk:items/pick_item
execute unless data storage rlk:pick pid run scoreboard players set #g tmp 2
execute unless data storage rlk:pick pid run function rlk:items/pick_item
execute unless data storage rlk:pick pid if score #gMax tmp matches 3.. run scoreboard players set #g tmp 3
execute unless data storage rlk:pick pid if score #gMax tmp matches 3.. run function rlk:items/pick_item
execute unless data storage rlk:pick pid if score #gMax tmp matches 4.. run scoreboard players set #g tmp 4
execute unless data storage rlk:pick pid if score #gMax tmp matches 4.. run function rlk:items/pick_item
