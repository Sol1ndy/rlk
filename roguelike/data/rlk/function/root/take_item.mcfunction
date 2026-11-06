# macro: h = 카드 순번 → rlk:room gid = 그 카드의 아이템
data remove storage rlk:room gid
$execute if data storage rlk:room rooti[$(h)] run data modify storage rlk:room gid set from storage rlk:room rooti[$(h)]
