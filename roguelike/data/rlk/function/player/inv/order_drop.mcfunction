# macro: ocur. 클릭되어 인벤에서 사라진 아이템을 발밑에 드롭 + 커서/조합칸 사본 제거 (@s = 플레이어)
$data modify storage rlk:gv id set value "$(ocur)"
execute at @e[tag=rlk_body,limit=1] run function rlk:items/drop with storage rlk:gv
data remove storage rlk:pinv obase
$data modify storage rlk:pinv obase set from storage rlk:items registry.$(ocur).item
execute if data storage rlk:pinv obase run function rlk:player/inv/order_drop_clear with storage rlk:pinv
