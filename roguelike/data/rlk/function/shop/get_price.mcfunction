# macro: rr(등급). 등급별 구매가 → io.price
$data modify storage rlk:io price set from storage rlk:shop buyprice.$(rr)
