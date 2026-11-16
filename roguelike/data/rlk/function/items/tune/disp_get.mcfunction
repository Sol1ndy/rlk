# macro: id → 설명 사본이 있으면 io.aq 를 그것으로
$execute if data storage rlk:items disp.$(id) run data modify storage rlk:io aq set from storage rlk:items disp.$(id)
