# 숄더뷰와 F5 시점 모두 사용자 기본 거리에서 다시 계산하므로 누적 확대가 없다.
function rlk:view/cam_calc
execute if entity @e[tag=rlk_vseat,limit=1] run function rlk:view/ride_apply
