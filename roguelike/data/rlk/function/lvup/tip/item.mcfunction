# 아이템 설명 = 이름 + 능력치/효과/설명 줄 + 각인 (macro: id)
$function rlk:lvup/ui/item_load {id:"$(id)"}
data modify storage rlk:lvpick tip append from storage rlk:io name
data modify storage rlk:lvpick lq set from storage rlk:io lore
function rlk:lvup/tip/lore_loop
