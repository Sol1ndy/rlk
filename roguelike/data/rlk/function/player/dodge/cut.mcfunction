# @s = 연출 잠금에 잡힌 플레이어(player/tick, 태그 rlk_mb_camh; 잠금의 둘째 틱부터 매 틱 — 첫 틱의 이동은 잠금이 시작되기 전 차례).
# round W (통합, wi_progress.md): 닷지 이동 · 웅크림 · 옆돌기의 대역 리그(박자가 돌지 않을 때)가 잠금 속으로 이어지지 않게 끝낸다.
# 대역 리그를 거두며 드러난 아바타는 같은 틱 뒤쪽의 char/cine/tick(hide)이 다시 숨긴다
scoreboard players set @s dashMoveT 0
execute if score #dgCr cb matches 1 run function rlk:player/dodge/stand
execute if score @s plActive matches 1 unless score #btK cb matches 1.. run function rlk:char/motion/lite/stop
