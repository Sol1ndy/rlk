# 화무십일홍: 대쉬한 틱 (@s = 플레이어, items/hook/on_dash ← player/dash_go). 대쉬 자체의 무적(dashInvT 6, player/tick 이 틱마다 1씩)이
# 남는 동안 = 지금부터 6틱 뒤까지(#hwDashEnd, gametime). 검신합일의 "대쉬로 흘려냄"은 이 동안만 센다(hw_ctr_q): 원소폭발 · 추락 ·
# 로노바 부활의 무적(같은 dashInvT 를 씀)은 대쉬가 아니다
execute store result score #hwDashEnd itv run time query gametime
scoreboard players add #hwDashEnd itv 6
