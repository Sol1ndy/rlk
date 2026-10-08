# @s = 문. 한쪽 구역이 지어질 때마다 한 단계: 0 숨김 → 1 닫힘 → 2 열림
execute if score @s dst matches ..1 run scoreboard players add @s dst 1
function rlk:room/door_draw
