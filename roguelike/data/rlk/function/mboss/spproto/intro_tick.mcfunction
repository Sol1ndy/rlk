# Hook intro_tick (@s = body; untargetable): 20 t, then the fight (music phase 1).
function rlk:mboss/spproto/rig/follow
execute if score #mbT mb matches 1 run function rlk:mboss/line/say {t:"균열 너머를 지킨다.",c:"#8FD8FF",gap:2,hold:24,snd:1}
execute if score #mbT mb matches 20.. run function rlk:mboss/spproto/start_fight
