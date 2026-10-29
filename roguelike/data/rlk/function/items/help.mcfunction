# items/give · items/drop {id:"help"} (macro: cmd = give | drop): 등록된 아이템 id 를 등급별로 (rlk:items ids = 등급순 정렬,
# items/register), 이어서 캐릭터 아이템 (rlk:codex chars, char/reg_items). 이름은 레지스트리의 name 을 그대로 읽는다
$function rlk:help/head {cmd:"/function rlk:items/$(cmd) {id:…}",what:"아이템 id (등급별)"}
$data modify storage rlk:help r set value {pre:'/function rlk:items/$(cmd) {id:"',post:'"}',st:"rlk:items",np:"registry.",ns:".name"}
data modify storage rlk:help rar set value ""
data modify storage rlk:help q set from storage rlk:items ids
function rlk:items/help_loop
function rlk:help/sub {title:"캐릭터"}
data modify storage rlk:help q set from storage rlk:codex chars
function rlk:help/list
execute store result score #hqN tmp run data get storage rlk:items ids
execute store result score #hqC tmp run data get storage rlk:codex chars
tellraw @s ["",{text:" 아이템 ",color:"gray"},{score:{name:"#hqN",objective:"tmp"},color:"white"},{text:"개 · 캐릭터 ",color:"gray"},{score:{name:"#hqC",objective:"tmp"},color:"white"},{text:"개 (채팅 창을 열고 위로 올려 보세요)",color:"gray"}]
data remove storage rlk:help r
data remove storage rlk:help rar
