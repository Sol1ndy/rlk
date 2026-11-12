# 각인 표시 만들기 (@s = 플레이어, 인벤이 바뀔 때 engravings/scan 에서 호출)
#   인벤토리 첫 줄 3~6번 칸: 개수가 같은 각인끼리 한 칸에 묶어, 개수 많은 묶음부터 왼쪽에. 아이템 개수 = 각인 개수,
#     설명은 묶음 안의 각인마다 켜진 효과만 밝게
#   7번 칸: 4묶음을 넘는 나머지 각인(이름과 개수). 나머지가 없으면 가진 각인 전체 요약
# 1) 개수 많은 순으로 정렬: 각인 목록을 한 번 훑어 개수(12 이상은 12)별 묶음 b.n1~n12 에 담고(묶음 안은 목록 순서),
#    n12 → n1 순서로 sorted 에 이어 붙인다 — 12 → 1 을 12번 훑던 예전 판과 같은 sorted({id, n}, 같은 개수는 목록 순서; 0 은 빠짐)
data modify storage rlk:eng b set value {n1:[],n2:[],n3:[],n4:[],n5:[],n6:[],n7:[],n8:[],n9:[],n10:[],n11:[],n12:[]}
data modify storage rlk:eng q set from storage rlk:engravings ids
function rlk:engravings/info_bucket_loop
data modify storage rlk:eng sorted set value []
execute if data storage rlk:eng b.n12[0] run data modify storage rlk:eng sorted append from storage rlk:eng b.n12[]
execute if data storage rlk:eng b.n11[0] run data modify storage rlk:eng sorted append from storage rlk:eng b.n11[]
execute if data storage rlk:eng b.n10[0] run data modify storage rlk:eng sorted append from storage rlk:eng b.n10[]
execute if data storage rlk:eng b.n9[0] run data modify storage rlk:eng sorted append from storage rlk:eng b.n9[]
execute if data storage rlk:eng b.n8[0] run data modify storage rlk:eng sorted append from storage rlk:eng b.n8[]
execute if data storage rlk:eng b.n7[0] run data modify storage rlk:eng sorted append from storage rlk:eng b.n7[]
execute if data storage rlk:eng b.n6[0] run data modify storage rlk:eng sorted append from storage rlk:eng b.n6[]
execute if data storage rlk:eng b.n5[0] run data modify storage rlk:eng sorted append from storage rlk:eng b.n5[]
execute if data storage rlk:eng b.n4[0] run data modify storage rlk:eng sorted append from storage rlk:eng b.n4[]
execute if data storage rlk:eng b.n3[0] run data modify storage rlk:eng sorted append from storage rlk:eng b.n3[]
execute if data storage rlk:eng b.n2[0] run data modify storage rlk:eng sorted append from storage rlk:eng b.n2[]
execute if data storage rlk:eng b.n1[0] run data modify storage rlk:eng sorted append from storage rlk:eng b.n1[]
# 2) 같은 개수끼리 묶기: groups = [{n, ids:[...]}] (sorted 가 많은 순이라 차례대로 묶으면 된다)
data modify storage rlk:eng groups set value []
data modify storage rlk:eng sq set from storage rlk:eng sorted
scoreboard players set #gn eng -1
function rlk:engravings/info_group_loop
# 3) 첫 줄 3~6번 칸: 묶음 하나씩
clear @s *[minecraft:custom_data~{rlk_engi:1b}]
scoreboard players set #slot eng 3
data modify storage rlk:eng gq set from storage rlk:eng groups
function rlk:engravings/info_gitem_loop
# 4) 7번 칸: 남은 묶음(gq)이 있으면 '그 밖의 각인', 없으면 전체 요약
data modify storage rlk:eng lore set value []
data modify storage rlk:eng sq set value []
execute if data storage rlk:eng gq[0] run function rlk:engravings/info_rest_sq
execute if data storage rlk:eng sq[0] run function rlk:engravings/info_sum_loop
execute if data storage rlk:eng lore[0] run data modify storage rlk:eng title set value "◆ 그 밖의 각인"
execute unless data storage rlk:eng lore[0] run data modify storage rlk:eng title set value "◆ 각인"
execute unless data storage rlk:eng lore[0] run data modify storage rlk:eng sq set from storage rlk:eng sorted
execute unless data storage rlk:eng lore[0] run function rlk:engravings/info_sum_loop
execute unless data storage rlk:eng lore[0] run data modify storage rlk:eng lore set value [{text:"가진 각인이 없습니다.",color:"gray",italic:false},{text:"같은 각인이 달린 아이템을 여러 개 모으면",color:"dark_gray",italic:false},{text:"효과가 켜집니다.",color:"dark_gray",italic:false}]
clear @s *[minecraft:custom_data~{rlk_eng:1b}]
function rlk:engravings/info_place with storage rlk:eng
execute store result score @s engItems run clear @s *[minecraft:custom_data~{rlk_engi:1b}] 0
