# 각인 표시 만들기 (@s = 플레이어, 인벤이 바뀔 때 engravings/scan 에서 호출)
#   자수정 조각(inventory.7): 가진 각인의 이름과 개수만
#   인벤토리 셋째 줄(inventory.18~26): 각인마다 아이템 하나 — 개수 많은 순, 아이템 개수 = 각인 개수, 설명은 켜진 효과만 밝게
#   9개를 넘는 나머지: 핫바 8번 칸(hotbar.8)에 이름과 개수만
# 1) 개수 많은 순으로 정렬: 12개 이상 → 11 → ... → 1 순서로 훑으며 sorted 에 담는다
data modify storage rlk:eng sorted set value []
scoreboard players set #want eng 12
data modify storage rlk:eng q set from storage rlk:engravings ids
function rlk:engravings/info_pass
scoreboard players set #want eng 11
data modify storage rlk:eng q set from storage rlk:engravings ids
function rlk:engravings/info_pass
scoreboard players set #want eng 10
data modify storage rlk:eng q set from storage rlk:engravings ids
function rlk:engravings/info_pass
scoreboard players set #want eng 9
data modify storage rlk:eng q set from storage rlk:engravings ids
function rlk:engravings/info_pass
scoreboard players set #want eng 8
data modify storage rlk:eng q set from storage rlk:engravings ids
function rlk:engravings/info_pass
scoreboard players set #want eng 7
data modify storage rlk:eng q set from storage rlk:engravings ids
function rlk:engravings/info_pass
scoreboard players set #want eng 6
data modify storage rlk:eng q set from storage rlk:engravings ids
function rlk:engravings/info_pass
scoreboard players set #want eng 5
data modify storage rlk:eng q set from storage rlk:engravings ids
function rlk:engravings/info_pass
scoreboard players set #want eng 4
data modify storage rlk:eng q set from storage rlk:engravings ids
function rlk:engravings/info_pass
scoreboard players set #want eng 3
data modify storage rlk:eng q set from storage rlk:engravings ids
function rlk:engravings/info_pass
scoreboard players set #want eng 2
data modify storage rlk:eng q set from storage rlk:engravings ids
function rlk:engravings/info_pass
scoreboard players set #want eng 1
data modify storage rlk:eng q set from storage rlk:engravings ids
function rlk:engravings/info_pass
# 2) 자수정 조각
data modify storage rlk:eng lore set value []
data modify storage rlk:eng sq set from storage rlk:eng sorted
function rlk:engravings/info_sum_loop
execute unless data storage rlk:eng lore[0] run data modify storage rlk:eng lore set value [{text:"가진 각인이 없습니다.",color:"gray",italic:false},{text:"같은 각인이 달린 아이템을 여러 개 모으면",color:"dark_gray",italic:false},{text:"효과가 켜집니다.",color:"dark_gray",italic:false}]
execute if data storage rlk:eng sorted[0] run data modify storage rlk:eng lore append value {text:"",italic:false}
execute if data storage rlk:eng sorted[0] run data modify storage rlk:eng lore append value {text:"각 각인의 효과는 아래 셋째 줄에서 볼 수 있습니다.",color:"dark_gray",italic:false}
clear @s *[minecraft:custom_data~{rlk_eng:1b}]
function rlk:engravings/info_place with storage rlk:eng
# 3) 셋째 줄
clear @s *[minecraft:custom_data~{rlk_engi:1b}]
scoreboard players set #slot eng 18
data modify storage rlk:eng sq set from storage rlk:eng sorted
function rlk:engravings/info_item_loop
# 4) 나머지 → 핫바 8번 칸
data modify storage rlk:eng lore set value []
function rlk:engravings/info_sum_loop
execute if data storage rlk:eng lore[0] run function rlk:engravings/info_rest with storage rlk:eng
execute store result score @s engItems run clear @s *[minecraft:custom_data~{rlk_engi:1b}] 0
