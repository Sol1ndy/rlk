# 낡은 석판 (@s = 플레이어, items/equip_scan 에서 호출). 보유 목록(rlk:pinv order = 인벤토리 둘째 줄 왼쪽부터, 셋째 줄로 이어짐)에서
# 석판의 바로 왼쪽·오른쪽 아이템의 스탯(그 아이템의 강화 배율 적용)을 #slatePct% 만큼 더한다. 석판 두 개 사이에 낀 아이템은 두 번 받는다
data modify storage rlk:scan sq set from storage rlk:pinv order
data modify storage rlk:scan prev set value ""
function rlk:items/slate/loop
