# Guard entry line; once per guard pair (cooldown 30 s).
execute if score #gdVoG mb matches 1.. run return 0
scoreboard players set #gdVoG mb 600
function rlk:mboss/line/say {t:"기록하여 판결할 지어다.",c:"#F2D488",gap:2,hold:40,snd:1}
