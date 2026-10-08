# 실행 위치에서 가장 가까운 상점 슬롯 제거(아이템·이름·버튼·블록·저장 모두)
# 사용: function rlk:shop/remove_nearest  (플레이어로 실행하면 가장 가까운 상점이 사라짐)
execute as @e[tag=rlk_shop_item,limit=1,sort=nearest] at @s positioned ~-0.5 ~-1.5 ~-0.5 align xyz run function rlk:shop/remove_slot_here
