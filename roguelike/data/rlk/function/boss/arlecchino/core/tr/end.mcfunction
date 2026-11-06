# T is over (or a reload / test finishes it; @s = body): P2, no floor; Q0 first (the decision picks it).
execute if score #trt kn matches 0 run function rlk:mboss/title {title:"두 세계 불의 잔재",sub:"페르엘",color:"#C8102E"}
execute if score #trt kn matches 0 run function rlk:boss/arlecchino/core/tr/title
execute if score #pat kn matches 51 run function rlk:boss/arlecchino/seq/t_p2/cancel
tag @s remove rlk_mb_inv
function rlk:mboss/cine/end
scoreboard players set #mbFloor mb 0
scoreboard players set #ph kn 5
scoreboard players set #pat kn 0
scoreboard players set #sq kn 0
scoreboard players set #sqdone kn 0
scoreboard players set #q0_ok kn 0
function rlk:boss/arlecchino/ai/phase
function rlk:boss/arlecchino/core/looks
function rlk:boss/arlecchino/ai/rec_start
scoreboard players set #rec kn 2
function rlk:boss/arlecchino/hud/sub
