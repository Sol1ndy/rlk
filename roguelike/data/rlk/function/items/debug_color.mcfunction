# macro: id. 능력이 있는데 impl 목록에 없으면 미구현 → 빨강, 아니면 흰색
data modify storage rlk:dbg col set value "white"
$execute if data storage rlk:items registry.$(id).abilities[0] unless data storage rlk:items {impl:["$(id)"]} run data modify storage rlk:dbg col set value "red"
