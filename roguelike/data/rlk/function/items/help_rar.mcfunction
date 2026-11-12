# macro: id. 앞 아이템과 등급이 다르면 (rlk:help rar 가 바뀌면) 등급 이름 줄 (rarity_kr · rarity_color)
$execute store success score #hqNew tmp run data modify storage rlk:help rar set from storage rlk:items registry.$(id).rarity
execute if score #hqNew tmp matches 0 run return 0
data modify storage rlk:help h set value {}
data modify storage rlk:help h.rar set from storage rlk:help rar
function rlk:items/help_rar_col with storage rlk:help h
function rlk:items/help_rar_line with storage rlk:help h
