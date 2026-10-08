# at = 블록 코너. rlk:pick pid → 표시(이름+설명) 구성 후 배치
data modify storage rlk:io id set from storage rlk:pick pid
function rlk:shop/place_build with storage rlk:io
