# 화무십일홍의 런 리셋 (@s = 플레이어, player/reset_one: 런 시작 · 런 실패 · rlk:reset · 로비 체험 정리 · 로비 수령). 다른 아이템의
# 타이머처럼 런마다 모든 상태를 지운다: hw_clear(중첩 · 적중 수 · 예약 · 치명타 확률 시간 · 사이드바) + 재사용 대기(검신합일 · 홍련일섬)
# + 대쉬 표시. 런 안에서 팔거나 버렸을 때는 hw_clear 만(재사용 대기는 남김)
function rlk:items/proc/hw_clear
scoreboard players set #hwCtrCd itv 0
scoreboard players set #hwSlCd itv 0
scoreboard players set #hwDashEnd itv 0
