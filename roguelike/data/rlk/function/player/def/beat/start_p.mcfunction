# 퍼펙트 패링의 박자를 시작한다 (@s = 플레이어, at 몸 eyes; player/def/fx/p3 = par3_go, 한 F 에 한 번; 태그 rlk_hc_atk = 공격한 적).
# 시간표(실제 틱, 0 = 맞은 틱; review/v/ref_pd.md 4 의 표): 0 접점 · 쨍 · 무기가 빛남 · 가드에서 쳐내기 시작 → 1 멈춤(히트 스톱) → 2 쳐낸 자세
# (런지) · 공격자가 뒤로 젖혀짐 · 별빛 · 가로 줄 · 따뜻한 화면 · 울림 → 3~5 멈춤 → 6 풀림(제 속도로 한 틱에): 별빛이 불꽃으로 깨짐 →
# 7~15 공격자 위를 기는 번개 → 12 무기의 빛이 꺼짐 → 17 끝. 세계는 1~5틱 동안 멈추고(5틱) 그동안 플레이어는 맞지 않는다.
# #btOn tmp 0 이면 세계를 멈추지 않고 효과만
execute if score #btK cb matches 1.. run function rlk:player/def/beat/end
scoreboard players set #btK cb 1
scoreboard players set #btA cb 0
scoreboard players set #btAct cb 0
tag @e[tag=rlk_hc_atk,limit=1] add rlk_bt_atk
# 접점(검이 만난 자리: 머리 높이, 적 쪽 0.65칸)을 표식으로 남긴다: 2틱의 별빛 · 6틱의 불꽃이 같은 자리
execute if entity @e[tag=rlk_hc_atk,limit=1] at @e[tag=rlk_body,limit=1] positioned ~ ~1.5 ~ facing entity @e[tag=rlk_hc_atk,limit=1] eyes positioned ^ ^ ^0.65 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_bt_pt","rlk_pet"]}
execute unless entity @e[tag=rlk_hc_atk,limit=1] at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] rotated ~ 0 positioned ~ ~1.5 ~ positioned ^ ^ ^0.65 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_bt_pt","rlk_pet"]}
execute at @e[type=minecraft:marker,tag=rlk_bt_pt,limit=1] run function rlk:player/def/fx/p3_at
# 아바타: 쳐내는 동작(리그 캐릭터의 클립 · 마네킹 캐릭터의 대역 리그)과 무기의 노란 빛
function rlk:char/motion/beat/parry
