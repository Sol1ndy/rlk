# @s = 플레이어, at 몸 eyes. 2단계 패링: 맞은 피해의 #parKeep2 %만(player/take_damage → par_keep), 넉백 · 피격 번쩍임 없음
scoreboard players set #parT tmp 2
execute unless score @s parHit = #now cb run function rlk:player/def/fx/p2
function rlk:player/def/par_use
tag @e[tag=rlk_hc_atk] remove rlk_hc_atk
