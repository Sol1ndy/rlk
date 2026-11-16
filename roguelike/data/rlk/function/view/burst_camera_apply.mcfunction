# F5 시점의 받침 거리를 사용자 기본 거리에서 다시 계산하므로 누적 확대가 없다.
execute if entity @e[tag=rlk_vseat,limit=1] run function rlk:view/ride_apply
