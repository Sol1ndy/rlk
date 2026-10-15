# 상점 노드의 진열대 8개 (위치 = 구역 한가운데 바닥 위). 앞줄 4 · 뒷줄 4, 칸 사이 3칸. 진열대 엔티티는 rlk_room 이라 맵이 바뀌면 사라진다
# 아이템 6개는 서로 다르게(이미 가진 아이템 제외), 등급 확률은 챕터와 상관없이 rlk:shop nodewt (레전더리까지)
data modify storage rlk:pick picked set value []
scoreboard players set #shopNode tmp 1
execute positioned ~-4.5 ~ ~-3.5 align xyz run function rlk:shop/node/item
execute positioned ~-1.5 ~ ~-3.5 align xyz run function rlk:shop/node/item
execute positioned ~1.5 ~ ~-3.5 align xyz run function rlk:shop/node/item
execute positioned ~4.5 ~ ~-3.5 align xyz run function rlk:shop/node/item
execute positioned ~-4.5 ~ ~3.5 align xyz run function rlk:shop/node/item
execute positioned ~-1.5 ~ ~3.5 align xyz run function rlk:shop/node/item
execute positioned ~1.5 ~ ~3.5 align xyz run function rlk:shop/node/heal_offer {id:"heal_s"}
execute positioned ~4.5 ~ ~3.5 align xyz run function rlk:shop/node/heal_offer {id:"heal_l"}
scoreboard players set #shopNode tmp 0
