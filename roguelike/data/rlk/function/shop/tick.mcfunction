# 상점: 상점 엔티티가 있을 때만 본처리(TPS 보호)
# 디버그: /scoreboard players set #shopOff tmp 1 로 상점 틱 전체 비활성화(랙 원인 분리용)
execute if score #shopOff tmp matches 1 run return 0
execute if entity @e[tag=rlk_shop_btn,limit=1] run function rlk:shop/tick_active
execute unless entity @e[tag=rlk_shop_btn,limit=1] if entity @e[tag=rlk_shop_reroll,limit=1] run function rlk:shop/tick_active
# 1초마다 슬롯 블록 확인(안산암/유리 파괴 시 상점 제거)
scoreboard players remove #shopChk tmp 1
execute if score #shopChk tmp matches ..0 if data storage rlk:shop slots[0] run function rlk:shop/check_blocks
