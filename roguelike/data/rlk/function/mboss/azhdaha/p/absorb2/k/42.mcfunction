# absorb2 #azPT 42
function rlk:mboss/azhdaha/look/tail
function rlk:mboss/azhdaha/arena/look_tail
function rlk:mboss/azhdaha/svc/banner_ab2
function rlk:mboss/line/say {t:"모락스! 너 정말 날 파멸시킬 작정이냐!",c:"#F2B53A",gap:2,hold:50,snd:2}
function rlk:mboss/azhdaha/svc/phase_3
function rlk:mboss/push/ring {r:80,to:85,kb:4}
execute if score #azTail mb matches 3 run function rlk:mboss/azhdaha/kstub/p/shard_rain/3
execute if score #azTail mb matches 4 run function rlk:mboss/azhdaha/kstub/p/shard_rain/4
execute if score #azTail mb matches 3 run function rlk:mboss/azhdaha/kstub/snd/absorb_burst/3
execute if score #azTail mb matches 4 run function rlk:mboss/azhdaha/kstub/snd/absorb_burst/4
