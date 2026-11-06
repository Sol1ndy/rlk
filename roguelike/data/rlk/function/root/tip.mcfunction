# 조준한 각인 카드의 설명 (@s = 플레이어, macro: h = rootc 의 순번) → rlk:lvpick tip
$execute unless data storage rlk:room rootc[$(h)] run return 0
$data modify storage rlk:lvpick b.e set from storage rlk:room rootc[$(h)]
data modify storage rlk:eng lore set value []
function rlk:invd/tip2_one with storage rlk:lvpick b
data modify storage rlk:eng lore append value {text:""}
data modify storage rlk:eng lore append value {text:"✦ 기적 (임시)",color:"#7CFC9A",bold:true}
data modify storage rlk:eng lore append value {text:"이 각인의 개수가 1 늘어난 것으로 칩니다.",color:"white"}
data modify storage rlk:eng lore append value {text:"카드 아래의 아이템도 함께 얻습니다.",color:"white"}
data modify storage rlk:eng lore append value {text:"(보유 칸이 가득하면 발밑에 놓입니다)",color:"dark_gray"}
data modify storage rlk:lvpick lq set from storage rlk:eng lore
execute if data storage rlk:lvpick lq[0] run data modify storage rlk:lvpick tip append from storage rlk:lvpick lq[0]
execute if data storage rlk:lvpick lq[0] run data remove storage rlk:lvpick lq[0]
function rlk:lvup/tip/lore_loop
# 함께 얻는 아이템의 설명
data remove storage rlk:lvpick c
$execute if data storage rlk:room rooti[$(h)] run data modify storage rlk:lvpick c.id set from storage rlk:room rooti[$(h)]
execute if data storage rlk:lvpick c.id unless data storage rlk:lvpick {c:{id:""}} run data modify storage rlk:lvpick tip append value {text:"\n\n함께 얻는 아이템\n",color:"#7CFC9A",bold:true}
execute if data storage rlk:lvpick c.id unless data storage rlk:lvpick {c:{id:""}} run function rlk:lvup/tip/item with storage rlk:lvpick c
