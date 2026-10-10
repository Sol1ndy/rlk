# 구역 건설 (@s = 구역 표식): 미리 만든 건설 함수(room/lz/<fn>_<테마>). 구역 종류는 드러나지 않는다(무늬 · 적 · 보상은 들어가야 나타남)
data modify storage rlk:room zbm.fn set from entity @s data.fn
data modify storage rlk:room zbm.n set from storage rlk:room th.n
execute if data entity @s data{boss_id:"narukami"} run function rlk:room/raiden/build
execute unless data entity @s data{boss_id:"narukami"} run function rlk:room/zb_fn with storage rlk:room zbm
scoreboard players set @s zst 1
# 이 구역에 붙은 문을 한 단계씩 진행(숨김→닫힘→열림)
scoreboard players operation #zb tmp = @s zid
execute as @e[tag=rlk_door] if score @s da = #zb tmp run function rlk:room/door_step
execute as @e[tag=rlk_door] if score @s db = #zb tmp run function rlk:room/door_step
