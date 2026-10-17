# 로그라이크 시스템 - 매 틱 실행
# 같은 효과음 겹침 방지 표시를 지움(build/psnd)
scoreboard players reset * snd
# uninstall 후에는 정지 (/reload 하면 다시 설치됨)
execute unless data storage rlk:config {installed:1b} run return 0
# ===== 'player' 태그 보유자만 시스템 적용. 2명 이상이면 전원 태그 제거 (인벤/아이템 저장소가 1인 기준) =====
execute store result score #pcount tmp if entity @a[tag=player]
execute if score #pcount tmp matches 2.. run tellraw @a [{"text":"[로그라이크] ","color":"red","bold":true},{"text":"'player' 태그는 한 명만 가질 수 있습니다. 전원 태그를 제거합니다.","color":"red"}]
execute if score #pcount tmp matches 2.. run tag @a[tag=player] remove player
execute if score #pcount tmp matches 2.. run return 0

# 시점 시스템(숄더뷰): 몸(rlk_body) 정하기 · 아바타 이동 · 카메라. 플레이어가 없으면 아바타 정리
# 이전 틱 피격의 남은 넉백을 카메라 갱신 전에 적용
execute as @e[tag=rlk_plkb] run function rlk:player/knockback/tick
# 평타 휘두르기 잠금(swHold): 이번 틱의 이동(view/move, 1인칭 속성)보다 먼저 atkCD 에서 다시 구한다
execute as @a[tag=player] run function rlk:player/swing/tick
execute as @a[tag=player] run function rlk:view/tick
execute unless entity @a[tag=player,limit=1] if entity @e[tag=rlk_view,limit=1] run kill @e[tag=rlk_view]
execute as @a[tag=player] run function rlk:player/tick
function rlk:combat/text_tick
# 화면 위 미니맵(리소스팩 글꼴, 보이지 않는 흰색 보스바 이름)
function rlk:minimap/tick
function rlk:ditem/tick
function rlk:shop/tick
# 화살(활 캐릭터)
execute as @e[tag=rlk_arrow] at @s run function rlk:char/bow/arrow_tick

# 몹 처리 (넉백저항·경직·체력바·상태이상)
execute as @e[type=!minecraft:player,type=!minecraft:item_display,type=!minecraft:block_display,type=!minecraft:text_display,type=!minecraft:interaction,type=!minecraft:marker,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:arrow,type=!minecraft:area_effect_cloud,type=!minecraft:item_frame,type=!minecraft:glow_item_frame,type=!minecraft:painting,tag=!rlk_mapv,tag=!rlk_mob,tag=!rlk_pet] at @s run function rlk:mob/setup
execute as @e[type=!minecraft:player,type=!minecraft:item_display,type=!minecraft:block_display,type=!minecraft:text_display,type=!minecraft:interaction,type=!minecraft:marker,type=!minecraft:item,type=!minecraft:experience_orb,type=!minecraft:arrow,type=!minecraft:area_effect_cloud,type=!minecraft:item_frame,type=!minecraft:glow_item_frame,type=!minecraft:painting,tag=!rlk_mapv,tag=rlk_mob] at @s run function rlk:mob/tick
# 어그로 유지: 0.5초마다 대상이 없는 몹을 다시 덤비게
scoreboard players add #aggT tmp 1
execute if score #aggT tmp matches 10.. run scoreboard players set #aggT tmp 0
execute if score #aggT tmp matches 0 as @e[tag=rlk_mob] run function rlk:mob/aggro_keep
# 체력바/빙결 정리: 몹 또는 체력바가 존재할 때만
execute if entity @e[tag=rlk_mob,limit=1] run function rlk:mob/hb_cleanup
execute unless entity @e[tag=rlk_mob,limit=1] if entity @e[tag=rlk_hb_bg,limit=1] run function rlk:mob/hb_cleanup
# 몹 클릭 실드: 존재할 때만 (고아 정리 + 클릭/우클릭 폴링)
execute if entity @e[tag=rlk_mshield,limit=1] run function rlk:combat/mshield_tick

# 커스텀 몹(cm): 두뇌 · 투사체 · 모습/부착물 정리
execute if entity @e[tag=rlk_cmb,limit=1] run function rlk:cm/world
execute unless entity @e[tag=rlk_cmb,limit=1] if entity @e[tag=rlk_cmglob,limit=1] run kill @e[tag=rlk_cmglob]
execute if entity @e[tag=rlk_cmp,limit=1] run function rlk:cm/pj/world
execute if entity @e[tag=rlk_cmlink,limit=1] run function rlk:cm/clean
# Narukami boss AI, telegraphs, combat objects and orphan cleanup.
execute if entity @e[tag=rlk_raiden,limit=1] run function rlk:boss/raiden/world
execute unless entity @e[tag=rlk_raiden,limit=1] if entity @e[tag=rlk_raiden_aux,limit=1] run function rlk:boss/raiden/cleanup
# 보스바는 서버 전체에 남으므로, 불러와진 나루카미가 없으면(런 종료·로비 복귀·청크 밖) 바로 숨긴다
execute if score #rdBar rd matches 1 unless entity @e[tag=rlk_raiden,limit=1] run function rlk:boss/raiden/bars_hide
# 회복구슬 / 아이템 소환물
execute as @e[tag=rlk_healorb] at @s run function rlk:combat/healorb_tick
execute as @e[tag=rlk_gold] at @s run function rlk:combat/gold_tick
function rlk:items/hook/tick_world
# 방 시스템: 런 진행 중 / 지도 등록 대기
execute if score #active room matches 1 run function rlk:room/tick
execute if score #setup room matches 1 as @a[tag=rlk_setup] if items entity @s weapon.mainhand minecraft:filled_map run function rlk:room/map_bind
function rlk:element/tick_world
# 원소 입자 / 캐릭터 소환물
execute as @e[tag=rlk_epart] at @s run function rlk:char/particle_tick
execute as @e[tag=rlk_jav] at @s run function rlk:char/lumine/jav_tick
# 나비아 금빛 카드 효과(tools/build_navia_fx_cards.py): 수명·보간·정리
function rlk:fx/nv/world

# 버려진 UI 아이템 제거: 바닥에 아이템 엔티티가 하나라도 있을 때만
execute if entity @e[type=minecraft:item,limit=1] run function rlk:cleanup_grounditems

# 눈앞 atkBlock/atkStrike 인터랙션 유지 + 클릭 폴링 (좌클릭=공격, 우클릭=대쉬)
execute as @a[tag=player] run function rlk:combat/atkblock_manage
# 대쉬 방향용 이전 위치 저장(다음 틱 델타)
execute as @a[tag=player] if entity @e[tag=rlk_body,limit=1] store result score @s dashPX run data get entity @e[tag=rlk_body,limit=1] Pos[0] 100
execute as @a[tag=player] if entity @e[tag=rlk_body,limit=1] store result score @s dashPZ run data get entity @e[tag=rlk_body,limit=1] Pos[2] 100
# 로비
function rlk:lobby/tick
