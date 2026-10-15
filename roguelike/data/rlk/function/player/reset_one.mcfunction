# @s = 플레이어. 개인 리셋: 레벨/스탯/골드/아이템/스택 (사파이어는 유지)
# 시작 캐릭터로
function rlk:char/start_reset
# 내려놓으려던 아이템 목록은 버린다(초기화라 떨구지 않음)
data modify storage rlk:lvpick dropq set value []
execute if score @s pkMode matches 1.. run function rlk:lvup/exit
function rlk:player/init
function rlk:lvup/init
scoreboard players set @s gold 0
scoreboard players set @s dice 0
scoreboard players set @s nodeHp 0
scoreboard players set @s invCap 9
# 아이템 전부 제거 + 인벤 시스템 상태 초기화
clear @s
data modify storage rlk:pinv order set value []
# 아이템 강화 단계 (id → 0~3)
data modify storage rlk:pinv enh set value {}
scoreboard players reset * enhL
function rlk:items/tune/reapply_all
# 세계수의 기적 받은 각인
data remove storage rlk:pinv mir
data remove storage rlk:pinv pcnt
function rlk:player/reset_stacks
function rlk:element/infuse_end
# 즉시 재스캔 + 체력 완충
function rlk:items/equip_scan
scoreboard players operation @s curHealth = @s maxHealth
scoreboard players set @s cxMode 0
