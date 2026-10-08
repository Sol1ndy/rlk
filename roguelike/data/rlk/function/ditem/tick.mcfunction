# 드롭 아이템 처리 (루트 tick)
# aimingDrop은 atkBlock 유지 로직(atkblock_manage)이 매 틱 참조하므로, 드롭 유무와 무관하게 반드시 리셋
scoreboard players set @a aimingDrop 0
# 회수 가능한 드롭 아이템이 하나라도 있을 때만 조준 레이캐스트/태그 스캔 처리
execute if entity @e[tag=rlk_ditem,limit=1] run function rlk:ditem/tick_active
