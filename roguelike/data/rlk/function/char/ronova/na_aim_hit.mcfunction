# 실행 위치 = 검사 상자의 최소 모서리. 이 조준선에서 처음 닿은 적 하나만 유도 대상으로 기록한다.
execute as @e[tag=rlk_mob,dx=0,dy=0,dz=0,sort=nearest,limit=1] unless score @s rnId matches 1.. run function rlk:element/void/assign_id
execute as @e[tag=rlk_mob,dx=0,dy=0,dz=0,sort=nearest,limit=1] run scoreboard players operation #rnAimTg tmp = @s rnId
tp @e[tag=rlk_rn_aim,limit=1] ~0.5 ~0.5 ~0.5
