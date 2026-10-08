# at = 슬롯 블록 코너. 이 슬롯의 엔티티(아이템/이름/버튼/라벨)만 정확한 위치로 제거 → 인접 슬롯 침범 방지
execute positioned ~0.5 ~1.5 ~0.5 run kill @e[tag=rlk_shop_item,distance=..0.3]
execute positioned ~0.5 ~3.05 ~0.5 run kill @e[tag=rlk_shop_info,distance=..0.3]
execute positioned ~0.5 ~2.35 ~0.5 run kill @e[tag=rlk_shop_btn,distance=..0.3]
execute positioned ~0.5 ~2.6 ~0.5 run kill @e[tag=rlk_shop_lbl,distance=..0.3]
