# order 재구성 (@s = 플레이어)
# 0) order 의 각 항목: 실물이 남아 있으면 유지, 없으면(클릭되어 커서로 감/버려짐) 월드 드롭 후 제거
data modify storage rlk:pinv neworder set value []
data modify storage rlk:pinv oscan set from storage rlk:pinv order
data remove storage rlk:pinv pcnt
function rlk:player/inv/order_rebuild_loop
data modify storage rlk:pinv order set from storage rlk:pinv neworder
# 1) order 에 없는 실물(새로 얻은 것) → order 뒤에 추가 (최대 invCap)
data modify storage rlk:pinv cscan set from storage rlk:items ids
function rlk:player/inv/collect_loop
