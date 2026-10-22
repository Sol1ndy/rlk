# macro: rr(등급). 등급별 구매가 → io.price
$data modify storage rlk:io price set from storage rlk:shop buyprice.$(rr)
# 상점 노드(맵의 상점 구역)는 따로 정한 값
$execute if score #shopNode tmp matches 1 run data modify storage rlk:io price set from storage rlk:shop nodeprice.$(rr)
