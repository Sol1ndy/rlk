# Hook intro_tick (@s = body, #mbT 1.. ; untargetable): 20 t, then the fight (proxies normal, music phase 1, the floor).
function rlk:mboss/cproto/rig/tick
execute if score #mbT mb matches 1 run function rlk:mboss/line/say {t:"챕터 보스 틀을 점검한다.",c:"#9FC6E8",gap:2,hold:24,snd:1}
execute if score #mbT mb matches 20.. run function rlk:mboss/cproto/start_fight
