# 슬롯 블록(안산암/유리) 파괴 감지 → 해당 상점 제거. 1초마다
scoreboard players set #shopChk tmp 20
data modify storage rlk:shop cscan set from storage rlk:shop slots
function rlk:shop/check_loop
