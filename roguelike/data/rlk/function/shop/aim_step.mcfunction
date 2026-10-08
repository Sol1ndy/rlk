# 통합 레이캐스트: 버튼 호버 + atkBlock 제거 + 이름 패널(설명) 한 번에
# 버튼 판정 = 레이 지점이 인터랙션 히트박스와 교차(dx/dy/dz)할 때만 → 유리 조준으로는 활성화 안 됨
# atkBlock 은 유지: 구매는 atkBlock 클릭 → on_attack → aim_buy 경로라 오히려 필요함
# 판정은 리롤 버튼과 완전히 동일(순수 히트박스 교차)
execute if entity @e[tag=rlk_shop_btn,dx=0,dy=0,dz=0] run tag @e[tag=rlk_shop_btn,dx=0,dy=0,dz=0,limit=1] add rlk_shop_hover
execute if entity @e[tag=rlk_shop_btn,dx=0,dy=0,dz=0] run return 0
execute if entity @e[tag=rlk_shop_reroll,dx=0,dy=0,dz=0] run tag @e[tag=rlk_shop_reroll,dx=0,dy=0,dz=0,limit=1] add rlk_shop_hover
execute if entity @e[tag=rlk_shop_reroll,dx=0,dy=0,dz=0] run return 0
execute if entity @e[tag=rlk_shop_info,distance=..1.2] run function rlk:shop/aim_info
execute if entity @e[tag=rlk_shop_info,distance=..1.2] run return 0
scoreboard players add #sray tmp 1
execute if score #sray tmp >= #rShop view run return 0
execute positioned ^ ^ ^0.35 run function rlk:shop/aim_step
