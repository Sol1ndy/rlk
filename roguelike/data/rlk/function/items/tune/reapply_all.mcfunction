# 모든 조정 상수를 지금 강화 단계로 다시 계산 (런 시작 때 강화 단계가 0 으로 돌아간 뒤)
data modify storage rlk:tune iq set from storage rlk:tune ids
function rlk:items/tune/reapply_loop
