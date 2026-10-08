# 반응 이름 표시 (실행 위치 위에, #rx = 반응 번호. 달 반응이면 #lunRx = 24 달 감전 / 25 달 개화 / 26 달 결정 이 대신 보인다)
scoreboard players operation #rxD tmp = #rx tmp
execute if score #lunRx tmp matches 24.. run scoreboard players operation #rxD tmp = #lunRx tmp
execute store result storage rlk:elem ri int 1 run scoreboard players get #rxD tmp
function rlk:element/rx_text2 with storage rlk:elem
