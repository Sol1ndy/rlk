# 도감용 등급별 목록 만들기 (도감을 열 때)
data modify storage rlk:codex byrar set from storage rlk:items byrar
data modify storage rlk:rb xq set from storage rlk:items box_exclude
function rlk:codex/lists_loop
