# 남은 묶음(gq)의 각인들을 sq = [{id,n}] 로 풀어 7번 칸 목록에 쓴다
execute unless data storage rlk:eng gq[0] run return 0
data modify storage rlk:eng gid set from storage rlk:eng gq[0].ids
function rlk:engravings/info_rest_sq2
data remove storage rlk:eng gq[0]
function rlk:engravings/info_rest_sq
