# 시작 모드에서 아이템을 고름 (@s = 플레이어): 지급하고 남은 선택 -1. 다 고르면 첫 맵으로
function rlk:codex/get_id
execute unless data storage rlk:codex t.id run return 0
function rlk:codex/start_take2 with storage rlk:codex t
