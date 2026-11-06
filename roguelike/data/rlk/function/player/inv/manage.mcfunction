# 인벤토리 슬롯 정리 (@s = 플레이어). 인벤 변화(dirty) 시에만 호출(개발자 모드에선 호출 안 됨)
# 배치: 첫 줄 = 캐릭터 · 상세 버튼 · 각인 · 스탯(frame 참고), 둘째·셋째 줄(inventory.9~26) = 얻은 아이템(invCap 칸, 획득순), 잠긴 칸은 방벽
# 보유 목록의 기준은 storage rlk:pinv order (아이템 id 리스트). 실물은 매번 order 에 맞춰 재배치됨
# 1) order ↔ 실물 동기화 (사라진 것 = 클릭해서 버림 → 월드 드롭 / 새로 들어온 것 → order 추가)
function rlk:player/inv/sync
# 2) 첫 줄 정리
function rlk:player/inv/frame
# 3) 얻은 아이템 배치 (inventory.9~, invCap 칸) + 잠긴 칸 방벽
function rlk:player/inv/place_items
# 4) 핫바 3~8번 · 커서에 잘못 놓인 아이템 청소
function rlk:player/inv/sweep_stray
