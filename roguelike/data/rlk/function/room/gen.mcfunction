# 맵 생성 (오버월드에서 실행. 입력: #mapType room). 이전 맵을 치우고 새 배치를 깐 뒤 첫 구역으로 이동
function rlk:room/clear
# 챕터 테마
function rlk:room/theme
# 맵 종류 → 배치 묶음
execute if score #mapType room matches 0 run function rlk:room/pick/first
# 노드 맵: 레벨업 노드가 있으면 첫 구역에 경험의 샘이 있는 레벨업 배치, 아니면 일반 배치
scoreboard players set #nLv tmp 0
execute if score #mapType room matches 1..7 if data storage rlk:room {next:[10]} run scoreboard players set #nLv tmp 1
execute if score #mapType room matches 1..7 if score #nLv tmp matches 1 run function rlk:room/pick/levelup
execute if score #mapType room matches 1..7 if score #nLv tmp matches 0 run function rlk:room/pick/normal
execute if score #mapType room matches 8 run function rlk:room/pick/boss
# 노드 맵(종류 1): 고른 선택지의 노드(rlk:room next)마다 서로 다른 중간 구역 하나를 그 노드 구역으로 + 제목
execute if score #mapType room matches 1..7 run function rlk:room/node/place
execute if score #mapType room matches 1..7 run function rlk:room/node/title
# 구역/문 표식 소환
data modify storage rlk:room q set from storage rlk:room cur.zones
function rlk:room/gen_zones
data modify storage rlk:room q set from storage rlk:room cur.doors
function rlk:room/gen_doors
# 첫 구역: 바로 건설 + 방문 처리
execute as @e[tag=rlk_zone,scores={zid=1}] run function rlk:room/zone_build
execute as @e[tag=rlk_zone,scores={zid=1}] at @s run function rlk:room/zone_first
# 낙사 구간: 바닐라 낙하 피해는 끈다(피해는 room/fall 이 준다)
attribute @a[tag=player,limit=1] minecraft:fall_damage_multiplier base set 0
# 걸음 높이는 기본값(1칸 단차는 점프)
attribute @a[tag=player,limit=1] minecraft:step_height base set 0.6
execute as @e[tag=rlk_av] run attribute @s minecraft:step_height base set 0.6
# 플레이어 이동 + 안내
execute as @a[tag=player,limit=1] run function rlk:room/gen_tp with storage rlk:room cur.spawn
execute store result storage rlk:room a.t int 1 run scoreboard players get #mapType room
execute as @a[tag=player,limit=1] run function rlk:room/gen_title with storage rlk:room a
# 화면 미니맵: 이 맵의 칸 → 구역 표
function rlk:minimap/build
