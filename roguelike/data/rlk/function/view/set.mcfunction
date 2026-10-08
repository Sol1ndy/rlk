# 카메라 위치 조절. 사용: /function rlk:view/set {right:0.9,up:0.3,back:3.3}
#   right = 아바타 머리에서 오른쪽으로(음수면 왼쪽), up = 위로, back = 뒤로 (칸). 소수점까지 적을 것
$data modify storage rlk:view cam set value {right:$(right)d,up:$(up)d,back:$(back)d}
function rlk:view/cam_calc
tellraw @s [{"text":"[시점] ","color":"gold","bold":true},{"text":"카메라 위치를 바꿨습니다.","color":"gray","bold":false}]
