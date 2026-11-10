# q_pf0 의 한 틱 전 판(바로 앞 틱에 퍼펙트 창이 열려 있었으면 성공)
execute store result score #qn cb run time query gametime
scoreboard players remove #qn cb 1
execute as @a[tag=player,limit=1] run return run function rlk:player/def/q_pf
return fail
