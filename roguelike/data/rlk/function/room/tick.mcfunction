# 방 시스템 매 틱 (런 진행 중일 때만 호출)
# 지도 아이템(왼손 지도 · 3번 칸 지도 버튼)은 더 주지 않는다: 화면 미니맵이 대신하고, 전체 지도는 G 메뉴로 연다.
# 이전 판에서 받은 지도가 남아 있으면 치운다.
execute as @a[tag=player,limit=1] if items entity @s weapon.offhand minecraft:filled_map[minecraft:custom_data~{rlk_map:1b}] run item replace entity @s weapon.offhand with air
execute as @a[tag=player,limit=1] if items entity @s hotbar.3 *[minecraft:custom_data~{rlk_ui:{role:"map"}}] run item replace entity @s hotbar.3 with air
# 플레이어 위치(×100, 직전 틱 기준)
scoreboard players operation #px tmp = @a[tag=player,limit=1] dashPX
scoreboard players operation #pz tmp = @a[tag=player,limit=1] dashPZ
# 전투 중이 아닐 때: 처음 들어간 구역 처리 / 닫힌 문에 다가가면 건너편 공개 (이 순서여야 방금 지은 구역에 같은 틱에 들어간 걸로 치지 않음)
execute if score #combat room matches 0 as @e[tag=rlk_zcell] if score #px tmp >= @s ex0 if score #px tmp <= @s ex1 if score #pz tmp >= @s ez0 if score #pz tmp <= @s ez1 run function rlk:room/cell_enter
execute if score #combat room matches 0 as @e[tag=rlk_door,scores={dst=1,dvis=1}] at @s if entity @e[tag=rlk_body,distance=..2.6] run function rlk:room/door_reveal
execute if score #combat room matches 1.. run function rlk:room/combat_tick
execute as @e[tag=rlk_wave] at @s run function rlk:room/wave_tick
execute if score #seal room matches 1 run function rlk:room/seal_all
# 레벨업 맵: 경험치 샘
execute as @e[tag=rlk_xpspot] at @s if entity @e[tag=rlk_body,distance=..8] run function rlk:room/xp/start
execute as @e[tag=rlk_xpsrc] at @s run function rlk:room/xp/tick
# 중간보스 아이템 상자(mboss/box): 떨어지는 연출 · 땅에 닿으면 오브젝트로 · 반짝임. 상자가 있을 때만(#mbBoxOn)
execute if score #mbBoxOn mb matches 1 run function rlk:mboss/box/all
# rift (build_rift.py)
execute if score #riftOn room matches 1 run function rlk:room/rift/tick
# 오브젝트 조준 표시 (주의: anchored eyes 로 시작점만 눈으로 옮기고 feet 으로 되돌려야 레이가 휘지 않음)
tag @e[tag=rlk_ohover] remove rlk_ohover
execute if entity @e[tag=rlk_obj,limit=1] as @a[tag=player,limit=1] at @s if entity @e[tag=rlk_obj,distance=..12] anchored eyes positioned ^ ^ ^0.01 anchored feet run function rlk:room/obj/aim
execute as @e[tag=rlk_obj] run function rlk:room/obj/hover

# 낙사 구간: 안전한 자리 기억 / 떨어진 플레이어·몹·아이템 처리
function rlk:room/fall/tick