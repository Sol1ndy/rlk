# macro: e = 각인 id. 이름 줄 (+ 세계수의 기적 표시) + 단계 설명
$data modify storage rlk:eng one set from storage rlk:engravings registry.$(e)
function rlk:engravings/info_gitem_name with storage rlk:eng one
$execute if data storage rlk:pinv {mir:"$(e)"} run data modify storage rlk:eng lore append value {text:"✦ 세계수의 기적: 개수 +1",color:"#7CFC9A",italic:false}
data modify storage rlk:eng tq set from storage rlk:eng one.tiers
function rlk:engravings/info_tiers
