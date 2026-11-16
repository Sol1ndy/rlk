# @s = 플레이어. 이번 닷지 동작의 이동 틱 수(#dgMv cb: 1 제자리 비틀기 3 · 3 내딛는 걸음 5 · 4 백스텝 4 · 2 옆돌기 6)와 단차 오르기 초기화
scoreboard players set @s dashMoveT 3
execute if score #dgMv cb matches 3 run scoreboard players set @s dashMoveT 5
execute if score #dgMv cb matches 4 run scoreboard players set @s dashMoveT 4
execute if score #dgMv cb matches 2 run scoreboard players set @s dashMoveT 6
scoreboard players set @s dashUpN 0
