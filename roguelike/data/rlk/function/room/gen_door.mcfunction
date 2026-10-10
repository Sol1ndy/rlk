# 문 표식: 두 구역 벽 사이 한가운데. 점수 da/db = 잇는 구역 번호, dst = 0 숨김 / 1 닫힘(검은 콘크리트) / 2 열림
$summon minecraft:marker $(mx).0 $(my) $(mz).0 {Tags:["rlk_room","rlk_door","rlk_new"]}
data modify entity @e[tag=rlk_new,limit=1] data set from storage rlk:room it
execute as @e[tag=rlk_new,limit=1] run function rlk:room/gen_door2
