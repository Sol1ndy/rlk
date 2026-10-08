# 구역 표식(marker): 구역 한가운데 바닥 위. 점수 = 번호/종류/상태, data = 구역 기록(칸·낙사 구간·장식). 칸마다 진입 판정용 표식(rlk_zcell)도 둔다
$summon minecraft:marker $(cx).0 201 $(cz).0 {Tags:["rlk_room","rlk_zone","rlk_new"]}
data modify entity @e[tag=rlk_new,limit=1] data set from storage rlk:room it
execute as @e[tag=rlk_new,limit=1] run function rlk:room/gen_zone2
data modify storage rlk:room cq set from storage rlk:room it.cells
function rlk:room/gen_cells
