# 화무십일홍의 할 일 (@s = 플레이어, hw_tick: 기다림 #hwWait 이 0): 지금 시각에 때가 된 것을 모두 처리하고 다음 시각(#hwNext)과
# 그때까지 남은 틱(#hwWait)을 다시 잡는다
execute store result score #hwNow itv run time query gametime
# 반격 예약(맞거나 닷지로 흘려낸 다음 처리: 피해 계산 도중에 새 피해를 주지 않음)
execute if score #hwCtrQ itv matches 1 at @e[tag=rlk_body,limit=1] run function rlk:items/proc/hw_ctr
# 육참골단 중첩 시간이 끝남 · 반격 재사용 대기 끝
execute if score #hwStk itv matches 1.. if score #hwNow itv >= #hwTEnd itv run function rlk:items/proc/hw_stk_end
execute if score #hwCtrCd itv matches 1 if score #hwNow itv >= #hwCtrEnd itv run scoreboard players set #hwCtrCd itv 0
# 홍련일섬: 시전 #hwSlDelay 틱 뒤 베기 · 치명타 확률 시간(10틱마다 불꽃, 끝) · 재사용 대기 끝(준비 신호)
execute if score #hwSlQ itv matches 1 if score #hwNow itv >= #hwSlAt itv at @e[tag=rlk_body,limit=1] run function rlk:items/proc/hw_slash
execute if score #hwCritT itv matches 1 if score #hwNow itv >= #hwSparkAt itv run function rlk:items/proc/hw_crit
execute if score #hwSlCd itv matches 1 if score #hwNow itv >= #hwSlEnd itv at @e[tag=rlk_body,limit=1] run function rlk:items/proc/hw_ready
# 다음 시각 = 남은 할 일 가운데 가장 이른 것(없으면 아주 먼 뒤)
scoreboard players set #hwNext itv 2147483647
execute if score #hwStk itv matches 1.. run scoreboard players operation #hwNext itv < #hwTEnd itv
execute if score #hwCtrCd itv matches 1 run scoreboard players operation #hwNext itv < #hwCtrEnd itv
execute if score #hwSlQ itv matches 1 run scoreboard players operation #hwNext itv < #hwSlAt itv
execute if score #hwCritT itv matches 1 run scoreboard players operation #hwNext itv < #hwSparkAt itv
execute if score #hwSlCd itv matches 1 run scoreboard players operation #hwNext itv < #hwSlEnd itv
scoreboard players operation #hwWait itv = #hwNext itv
scoreboard players operation #hwWait itv -= #hwNow itv
# 남은 할 일이 있으면 상태가 있는 것: 팔거나 버리면 hw_clear 가 기다림을 0 으로(다시 가지면 첫 틱에 다시 봄)
execute if score #hwNext itv matches ..2147483646 run scoreboard players set #hwOn itv 1
