# @s = 플레이어, at 몸 eyes. 퍼펙트 패링의 보상과 효과(한 F 에 한 번)
scoreboard players operation #cut cb = #parCut tmp
function rlk:char/cd_cut
# 균형치는 그 적의 자리에서 깎는다(마지막 칸이면 그로기가 거기서 시작: 취소할 공격 소품 · 섬광의 자리)
execute as @e[tag=rlk_hc_atk,limit=1] at @s run function rlk:bal/hit {n:1}
function rlk:player/def/fx/p3
function rlk:items/hook/on_parry
