# 사용: /function rlk:view/ride_set {d:4.5,s:1.0}  (d = 카메라 거리 칸, s = 받침 크기: 머리 위로 약 s 칸)
$data modify storage rlk:view ride set value {d:$(d)d,s:$(s)d}
function rlk:view/ride_apply
