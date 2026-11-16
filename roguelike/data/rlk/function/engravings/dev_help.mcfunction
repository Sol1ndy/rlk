# engravings/dev {id:"help",n:0}: 등록된 각인 id 와 이름 (rlk:engravings ids · registry.<id>.name, engravings/register)
function rlk:help/head {cmd:"/function rlk:engravings/dev {id:…,n:…}",what:"각인 id (n = 더할 개수, 0 = 해제)"}
data modify storage rlk:help r set value {pre:'/function rlk:engravings/dev {id:"',post:'",n:4}',st:"rlk:engravings",np:"registry.",ns:".name"}
data modify storage rlk:help q set from storage rlk:engravings ids
function rlk:help/list
data remove storage rlk:help r
