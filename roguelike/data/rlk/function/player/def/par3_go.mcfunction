# @s = 플레이어, at 몸 eyes. 퍼펙트 패링의 보상과 효과(한 F 에 한 번)
scoreboard players operation #cut cb = #parCut tmp
function rlk:char/cd_cut
execute as @e[tag=rlk_hc_atk,limit=1] run function rlk:bal/hit {n:1}
function rlk:player/def/fx/p3
function rlk:items/hook/on_parry
