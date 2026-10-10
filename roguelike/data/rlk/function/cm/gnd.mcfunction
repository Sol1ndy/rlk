# 실행 위치에서 아래로 바닥을 찾아(최대 12칸) 그 윗면에 표시 $(k). 입력: #cmK(묶음 번호) · #wdT(차오르는 틱)
scoreboard players set #rl tmp 0
$function rlk:cm/gnd_dn {k:"$(k)"}
