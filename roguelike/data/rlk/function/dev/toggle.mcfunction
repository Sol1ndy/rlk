# 개발자 모드 토글 (@s = 플레이어). 사용: /function rlk:dev/toggle
# ON: 핫바/인벤 슬롯 고정 해제, 클릭 감지 인터랙션 제거(블록 설치·파괴 등 자유 조작), 핫바 0번이 아니어도 공격 판정
execute if score @s devMode matches 1 run return run function rlk:dev/off
function rlk:dev/on
