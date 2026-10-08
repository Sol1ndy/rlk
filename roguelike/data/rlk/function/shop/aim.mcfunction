# @s = 플레이어, at 눈(anchored eyes). 상점 버튼/이름 패널 조준 레이캐스트
# 주의: anchored eyes 유지 상태로 ^ ^ ^ 재귀를 돌리면 스텝마다 눈높이가 재적용돼 레이가 위로 휨
# → 시작점을 눈으로 옮긴 뒤 anchored feet 으로 리셋하고 순수 방향 스텝만 사용
scoreboard players set #sray tmp 0
execute positioned ^ ^ ^0.01 anchored feet run function rlk:shop/aim_step
