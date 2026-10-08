# macro: rcx, rcy, rcz. 해당 슬롯에서 재추첨. align으로 블록 코너에 스냅(정수 좌표 중앙 보정 방지)
$execute positioned $(rcx) $(rcy) $(rcz) align xyz run function rlk:shop/respawn_slot
