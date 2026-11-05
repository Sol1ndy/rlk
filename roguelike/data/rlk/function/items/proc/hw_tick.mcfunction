# 화무십일홍 매 틱 (@s = 플레이어, 가지고 있는 동안, items/hook/tick_player): 다음 할 일까지 남은 틱(#hwWait)만 줄이고, 0 이 되면 hw_due
# (할 일 = 중첩이 끝남 · 예약된 반격 · 반격 재사용 대기 끝 · 홍련일섬 베기 · 치명타 확률 시간의 불꽃 · 끝 · 홍련일섬 준비. 타이머는 끝나는
# 시각(gametime)을 적어 두는 방식이라 매 틱 하는 일은 이것뿐: 가지고 있는 동안 틱당 명령 수가 늘 같다)
scoreboard players remove #hwWait itv 1
execute if score #hwWait itv matches ..0 run function rlk:items/proc/hw_due
