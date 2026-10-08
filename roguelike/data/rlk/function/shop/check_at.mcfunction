# macro: ccx,ccy,ccz. 안산암 또는 유리가 없으면 그 상점 제거(중복 실행 방지 위해 분기). align으로 코너 스냅
$execute positioned $(ccx) $(ccy) $(ccz) align xyz unless block ~ ~ ~ minecraft:polished_andesite run function rlk:shop/remove_slot_here
$execute positioned $(ccx) $(ccy) $(ccz) align xyz if block ~ ~ ~ minecraft:polished_andesite unless block ~ ~1 ~ minecraft:glass run function rlk:shop/remove_slot_here
