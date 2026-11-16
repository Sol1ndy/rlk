# @s = 플레이어, at 몸 eyes. 1단계 패링: 맞은 피해의 #parKeep1 %만(player/take_damage → par_keep), 넉백 · 피격 번쩍임 없음
scoreboard players set #parT tmp 1
execute unless score @s parHit = #now cb run function rlk:player/def/fx/p1
function rlk:player/def/par_use
