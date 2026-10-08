# 카메라가 따라오는 느낌 조절. 사용: /function rlk:view/tune {smooth:1,lead:0}
#   smooth = 카메라 위치를 몇 틱에 걸쳐 부드럽게 옮길지(0~3). 작을수록 마우스를 빨리 따라오지만 걸을 때 덜 부드러움
#   lead   = 회전 예측(0~3 틱). 마우스를 돌리는 속도만큼 카메라를 미리 보냄. 클수록 빨리 따라오지만 멈출 때 살짝 출렁일 수 있음
$data modify storage rlk:view opt set value {smooth:$(smooth),lead:$(lead)}
function rlk:view/tune_apply
tellraw @s [{"text":"[시점] ","color":"gold","bold":true},{"text":"카메라 따라오기 설정을 바꿨습니다.","color":"gray","bold":false}]
