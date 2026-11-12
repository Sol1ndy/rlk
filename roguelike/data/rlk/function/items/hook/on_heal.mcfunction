# 치유를 받기 직전 (@s = 플레이어, #heal tmp = 치유량 — 여기서 늘리거나 0 으로 만들 수 있다)
# 중간보스 전투 중: 치유 시도 1회를 기록(#mbHealEv)하고 받는 치유 보정(#mbHealPct, 달빛 고치 −40%). 캐릭터 변환보다 먼저
execute if score #mbLive mb matches 1 if score #heal tmp matches 1.. run function rlk:mboss/player_heal
# 캐릭터: 치유를 다른 것으로 바꾸는 상태
function rlk:char/heal_hook
# 기도 묵주: 받는 치유량 증가
execute if score @s it_prayer_beads matches 1.. if score #heal tmp matches 1.. run function rlk:items/proc/beads
