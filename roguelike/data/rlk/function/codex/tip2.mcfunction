# 각인 설명 창: 조준한 아이템의 각인(인벤토리 상세와 같은 내용). 아이템을 보고 있지 않으면 비운다
data modify storage rlk:eng lore set value []
execute if score @s pkHK matches 13 if data storage rlk:codex t.id run function rlk:invd/tip2_engs with storage rlk:codex t
data modify storage rlk:lvpick tip set value []
data modify storage rlk:lvpick lq set from storage rlk:eng lore
execute if data storage rlk:lvpick lq[0] run data modify storage rlk:lvpick tip append from storage rlk:lvpick lq[0]
execute if data storage rlk:lvpick lq[0] run data remove storage rlk:lvpick lq[0]
function rlk:lvup/tip/lore_loop
execute if data storage rlk:lvpick tip[0] run function rlk:invd/tip2_set with storage rlk:lvpick
execute unless data storage rlk:lvpick tip[0] run data modify entity @e[tag=rlk_pk_tip2,limit=1] text set value {text:""}
