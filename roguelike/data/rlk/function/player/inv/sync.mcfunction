# order 재구성 (@s = 플레이어)
# 0) order 의 각 항목: 실물이 남아 있으면 유지, 없으면(클릭되어 커서로 감/버려짐) 월드 드롭 후 제거
data modify storage rlk:pinv neworder set value []
data modify storage rlk:pinv oscan set from storage rlk:pinv order
data remove storage rlk:pinv pcnt
execute store result score #syO tmp run data get storage rlk:pinv order
function rlk:player/inv/order_rebuild_loop
data modify storage rlk:pinv order set from storage rlk:pinv neworder
# 1) order 에 없는 실물(새로 얻은 것) → order 뒤에 추가 (최대 invCap)
#    빠른 길: 0) 에서 버린 항목이 없고(길이 그대로) 실물(인벤 + 핫바의 rlk 아이템) 수 = order 길이면, 모든 실물이 이미 order 항목과
#    짝지어져(order_keep 이 항목마다 하나씩 뺌) 더할 것이 없다 — 등록된 모든 id 를 훑는 collect_loop 를 건너뜀(결과 같음)
execute store result score #syN tmp run data get storage rlk:pinv order
execute store result score #syP tmp if items entity @s inventory.* *[minecraft:custom_data~{rlk:{}}]
execute store result score #syH tmp if items entity @s hotbar.* *[minecraft:custom_data~{rlk:{}}]
scoreboard players operation #syP tmp += #syH tmp
execute if score #syN tmp = #syO tmp if score #syP tmp = #syN tmp run return 0
data modify storage rlk:pinv cscan set from storage rlk:items ids
function rlk:player/inv/collect_loop
