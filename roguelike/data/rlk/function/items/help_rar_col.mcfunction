# macro: rar -> rlk:help h.col (등급 색), h.kr (등급 한글 이름; 없으면 등급 id)
$data modify storage rlk:help h.col set from storage rlk:items rarity_color.$(rar)
$data modify storage rlk:help h.kr set value "$(rar)"
$data modify storage rlk:help h.kr set from storage rlk:items rarity_kr.$(rar)
execute unless data storage rlk:help h.col run data modify storage rlk:help h.col set value "gold"
