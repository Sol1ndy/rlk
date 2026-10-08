# 조준한 도감 아이템의 설명 (@s = 플레이어, pkHI = 이 쪽 안의 순번)
function rlk:codex/get_id
execute if data storage rlk:codex t.id run function rlk:lvup/tip/item with storage rlk:codex t
