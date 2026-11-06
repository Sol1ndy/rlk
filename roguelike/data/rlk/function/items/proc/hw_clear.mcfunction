# 화무십일홍을 팔거나 버렸을 때 (@s = 플레이어, items/hook/tick_player: 더는 가지고 있지 않고 상태가 남은 첫 틱)
# 중첩 · 적중 수 · 예약 · 치명타 확률 시간 · 사이드바를 지운다. 재사용 대기(#hwCtrCd · #hwSlCd 와 끝나는 시각)는 남긴다:
# 버렸다가 다시 주워도 홍련일섬의 재사용 대기가 없어지지 않고, 끝나는 시각이 지나 있으면 다시 가진 첫 틱에 풀린다
scoreboard players set #hwOn itv 0
scoreboard players set #hwHits itv 0
scoreboard players set #hwStk itv 0
scoreboard players set #hwAtk itv 0
scoreboard players set #hwCtrQ itv 0
scoreboard players set #hwSlQ itv 0
scoreboard players set #hwCritT itv 0
scoreboard players set #hwPulse itv 0
scoreboard players reset 육참골단 stacks
# 다시 가지면 첫 틱에 할 일을 다시 본다(가지지 않은 동안 #hwWait 은 줄지 않으므로)
scoreboard players set #hwWait itv 0
