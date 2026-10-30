# char/select {id:"help"}: 등록된 캐릭터 (rlk:codex chars = 캐릭터 아이템 char_<id> 목록, char/reg_items; 아이템의 char = 캐릭터 id,
# 이름 = rlk:chars registry.<id>.info.name)
function rlk:help/head {cmd:"/function rlk:char/select {id:…}",what:"캐릭터 id"}
data modify storage rlk:help r set value {pre:'/function rlk:char/select {id:"',post:'"}',st:"rlk:chars",np:"registry.",ns:".info.name"}
data modify storage rlk:help q set from storage rlk:codex chars
function rlk:char/select_help_loop
data remove storage rlk:help r
