# 맵 생성 (오버월드에서 실행. 입력: #mapType room). 이전 맵을 치우고 새 배치를 깐 뒤 첫 구역으로 이동
function rlk:room/clear
# 챕터 테마
function rlk:room/theme
# 맵 종류 → 배치 묶음
execute if score #mapType room matches 0 run function rlk:room/pick/first
execute if score #mapType room matches 1..3 run function rlk:room/pick/normal
execute if score #mapType room matches 6..7 run function rlk:room/pick/normal
execute if score #mapType room matches 4 run function rlk:room/pick/levelup
execute if score #mapType room matches 5 run function rlk:room/pick/root
execute if score #mapType room matches 8 run function rlk:room/pick/boss
# 이점 구역: 중간 구역 하나를 특수 구역으로 (돈 3, 상점 4, 사파이어 5, 재련 6, 인챈트 7)
scoreboard players set #special tmp 0
execute if score #mapType room matches 1 run scoreboard players set #special tmp 3
execute if score #mapType room matches 2 run scoreboard players set #special tmp 4
execute if score #mapType room matches 3 run scoreboard players set #special tmp 5
execute if score #mapType room matches 6 run scoreboard players set #special tmp 6
execute if score #mapType room matches 7 run scoreboard players set #special tmp 7
execute if score #special tmp matches 1.. run function rlk:room/gen_special
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
