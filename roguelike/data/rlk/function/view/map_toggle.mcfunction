# 지도 버튼/G 메뉴. 같은 클릭의 중복 처리 방지; 슬롯 선택만으로는 열지 않는다.
execute if score @s vMapH matches 1.. run return 0
execute if score @s vMap matches 1 run return run function rlk:view/map_close
function rlk:view/map_open
