# 조준한 보유 아이템의 각인 설명 (@s = 플레이어). 아이템을 보고 있지 않으면 비운다
data modify storage rlk:eng lore set value []
execute if score @s pkHK matches 2 run function rlk:invd/tip2_item with storage rlk:lvpick a
data modify storage rlk:lvpick tip set value []
data modify storage rlk:lvpick lq set from storage rlk:eng lore
execute if data storage rlk:lvpick lq[0] run data modify storage rlk:lvpick tip append from storage rlk:lvpick lq[0]
execute if data storage rlk:lvpick lq[0] run data remove storage rlk:lvpick lq[0]
function rlk:lvup/tip/lore_loop
function rlk:invd/tip2_set with storage rlk:lvpick
