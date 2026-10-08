# macro: ocur. 해당 id 의 실물 개수(메인 인벤 + 핫바, 커서 제외)를 pcnt.<id> 에 저장
data remove storage rlk:pinv cbase
$data modify storage rlk:pinv cbase set from storage rlk:items registry.$(ocur).item
$data modify storage rlk:pinv ccnt set value "$(ocur)"
execute if data storage rlk:pinv cbase run function rlk:player/inv/order_count2 with storage rlk:pinv
