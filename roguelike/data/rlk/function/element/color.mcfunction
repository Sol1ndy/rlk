# #elem 에 맞는 대미지 숫자 색을 storage rlk:combat col/sc1/sc2 에 설정
execute store result storage rlk:elem ci int 1 run scoreboard players get #elem tmp
function rlk:element/color2 with storage rlk:elem
