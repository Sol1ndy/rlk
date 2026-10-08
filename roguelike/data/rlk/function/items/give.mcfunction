# ID로 아이템 지급 (@s = 받는 플레이어). 사용: function rlk:items/give {id:"sealed_sword"}
data remove storage rlk:io src
$data modify storage rlk:io src set from storage rlk:items registry.$(id)
$data modify storage rlk:io id set value "$(id)"
data remove storage rlk:io clickdrop
execute if data storage rlk:io src.item run function rlk:items/give_do
