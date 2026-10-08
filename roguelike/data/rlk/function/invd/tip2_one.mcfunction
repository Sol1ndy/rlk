# macro: e = 각인 id. "◆ 이름  n개" + 단계별 설명(지금 개수로 켜진 줄만 밝게)
$execute store result score #n tmp run scoreboard players get $(e) engN
$data modify storage rlk:eng cur set from storage rlk:engravings registry.$(e)
execute store result storage rlk:eng cur.n int 1 run scoreboard players get #n tmp
execute if data storage rlk:eng lore[0] run data modify storage rlk:eng lore append value {text:""}
function rlk:engravings/info_head with storage rlk:eng cur
data modify storage rlk:eng tq set from storage rlk:eng cur.tiers
function rlk:engravings/info_tiers
