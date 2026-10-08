# 구역 건설 (@s = 구역 표식). 칸마다 바닥·벽 → 바닥·벽 무늬 → 낙사 구간 → 프롭. 구역 종류는 드러나지 않는다(무늬·적·보상은 들어가야 나타남)
# 이 구역에 붙은 문을 한 단계씩 진행(숨김→닫힘→열림)
data modify storage rlk:room zb set from entity @s data
data modify storage rlk:room q set from storage rlk:room zb.cells
function rlk:room/zb_cells
function rlk:room/zb_list {l:"a"}
function rlk:room/deco_loop
data modify storage rlk:room q set from storage rlk:room zb.pits
function rlk:room/zb_pit_walls
data modify storage rlk:room q set from storage rlk:room zb.pits
function rlk:room/zb_pit_holes
function rlk:room/zb_list {l:"b"}
function rlk:room/deco_loop
scoreboard players set @s zst 1
scoreboard players operation #zb tmp = @s zid
execute as @e[tag=rlk_door] if score @s da = #zb tmp run function rlk:room/door_step
execute as @e[tag=rlk_door] if score @s db = #zb tmp run function rlk:room/door_step
