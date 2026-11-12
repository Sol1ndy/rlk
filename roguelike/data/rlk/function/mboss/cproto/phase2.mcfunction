# The phase-1 floor was reached (#mbFloorHit 1): the second pool (40 % of #mbTot), the title swap, the phase-2 music,
# a 20-t cine (boss hits refused); phase 2 has no floor.
scoreboard players set #cpPh mb 2
scoreboard players set #mbFloor mb 0
scoreboard players set #mbFloorHit mb 0
function rlk:mboss/repool {pct:40}
function rlk:mboss/title {title:"시험용 수호자 · 2단계",sub:"챕터 보스 틀 점검용",color:"#E8A0A0"}
function rlk:mboss/music/set {ph:2}
function rlk:mboss/cine/start
scoreboard players set #cpCine mb 20
function rlk:mboss/lib_clear
scoreboard players set #cpPat mb 0
function rlk:mboss/line/say {t:"두 번째 판이다.",c:"#9FC6E8",gap:2,hold:30,snd:2}
