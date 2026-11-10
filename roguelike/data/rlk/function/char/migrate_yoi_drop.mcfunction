# @s = 바닥에 떨어진 요이미야 캐릭터 카드(rlk_ditem): 그 묶음(카드 · 정보 · 버튼 · 이름표 · 기록)을 치운다
execute store result storage rlk:mig dg.dg int 1 run scoreboard players get @s dgid
function rlk:ditem/kill_group with storage rlk:mig dg
data remove storage rlk:mig dg
