execute if score @s rdCam matches 1 run scoreboard players set @s dashMoveT 0
execute if score @s rdCam matches 1 run scoreboard players set @s stepT 0
# 플레이어별 매 틱 처리 (@s = 플레이어)

# 아직 초기화되지 않았으면 초기화
execute unless score @s init matches 1 run function rlk:player/init
# 이전 버전에서 넘어온 플레이어(레벨 없음)는 다시 초기화
execute unless score @s level matches 1.. run function rlk:player/init
execute unless score @s invCap matches 9..18 run scoreboard players set @s invCap 9

# 상시 야간투시: 입자 없이 무한 유지. 사망/효과 해제 뒤에도 자동 복구.
execute unless data entity @s active_effects[{id:"minecraft:night_vision",duration:-1}] run effect give @s minecraft:night_vision infinite 0 true

# 이름이 바뀐 아이템(페보니우스 활 → 비전) 교체
execute if items entity @s container.* *[minecraft:custom_data~{rlk:{id:"favonius_bow"}}] run function rlk:items/migrate_p
# ===== 인벤 변화 감지(dirty): 인벤 정렬·장비 스캔은 변화 시에만 =====
# 프로브: rlk 아이템 총 개수. 변하면 dirty (클릭→커서 이동도 개수 변화로 감지됨)
execute store result score #ic tmp if items entity @s inventory.* *[minecraft:custom_data~{rlk:{}}]
execute store result score #ic2 tmp if items entity @s hotbar.* *[minecraft:custom_data~{rlk:{}}]
scoreboard players operation #ic tmp += #ic2 tmp
execute unless score #ic tmp = @s invCnt run scoreboard players set @s invDirty 2
scoreboard players operation @s invCnt = #ic tmp
# 발전과제 이벤트(inventory_changed) → dirty
execute if score @s invEvt matches 1.. run scoreboard players set @s invDirty 2
# 폴백: 10초마다 강제 1회
scoreboard players remove @s manageTick 1
execute if score @s manageTick matches ..0 run scoreboard players set @s invDirty 2
execute if score @s manageTick matches ..0 run scoreboard players set @s manageTick 200
# dirty일 때만: 인벤 정렬(개발자 모드에선 생략) + 무거운 장비 스캔
execute unless score @s devMode matches 1 if score @s invDirty matches 1.. run function rlk:player/inv/manage
execute if score @s invDirty matches 1.. run function rlk:items/equip_scan
execute if score @s invDirty matches 1.. run scoreboard players remove @s invDirty 1

# 버프성 스탯(증가/증폭)은 2틱마다 가벼운 패스로
scoreboard players remove @s scanTick 1
execute if score @s scanTick matches ..0 run function rlk:items/stat_light
function rlk:player/apply_attributes
function rlk:player/health_tick
function rlk:player/hunger
function rlk:player/update_item
function rlk:player/level/bar
# 핫바 잠금
execute at @s run function rlk:player/hotbar/tick

# 공격 쿨다운 / 콤보 유지시간
execute if score @s uiCd matches 1.. run scoreboard players remove @s uiCd 1
execute if score @s atkCD matches 1.. run scoreboard players remove @s atkCD 1
scoreboard players add @s cboIdle 1
execute if score @s pmActive matches 1 if score @s atkCD matches 1.. run scoreboard players set @s cboIdle 0
execute if score @s cboIdle matches 20.. run scoreboard players set @s comboStep 0

# 대쉬: 자체 쿨 / 충전 / 무적 / 이동
execute if score @s dashCool matches 1.. run scoreboard players remove @s dashCool 1
execute if score @s dashCharge < #dashMax tmp run function rlk:player/dash_regen
execute if score @s dashInvT matches 1.. run scoreboard players remove @s dashInvT 1
execute if score @s dashMoveT matches 1.. at @e[tag=rlk_body,limit=1] rotated ~ 0 run function rlk:player/dash_move_tick
# 살짝 전진(찌르기 등). 대쉬가 시작되면 멈춘다
execute if score @s dashMoveT matches 1.. run scoreboard players set @s stepT 0
execute if score @s stepT matches 1.. at @e[tag=rlk_body,limit=1] rotated ~ 0 run function rlk:player/step_move_tick

# 레벨 업 아이템 선택
function rlk:lvup/tick
# 인벤토리 상세 버튼
execute unless score @s devMode matches 1 run function rlk:invd/tick
# 캐릭터(스킬 재사용 대기·원소 에너지·캐릭터별 처리)
execute if score @s pmActive matches 1 if score @s dead matches 1 run function rlk:char/motion/stop
execute if score @s pmActive matches 1 if score @s vMap matches 1 run function rlk:char/motion/stop
execute if score @s pmActive matches 1 if score @s pkMode matches 1.. run function rlk:char/motion/stop
function rlk:char/tick
# 생명의 계약 표시
function rlk:player/bol/tick
# 원소(부여 시간·방어막·부착/반응)
function rlk:player/elem_tick
# 액션바 HUD (대쉬 충전 게이지, 항상 표시)
function rlk:player/hud/tick

# 아이템 틱(타이머/변신/사이드바)
function rlk:items/hook/tick_player
# 각인(보호막·심연의 원소 등)
function rlk:engravings/tick
# 보호막 이펙트(숄더뷰에서만)
function rlk:view/shield_fx

# 디버그 trigger (아이템 목록에서 클릭 → 드롭 / 페이지 이동)
scoreboard players enable @s dbgDropI
scoreboard players enable @s dbgPage
execute if score @s dbgDropI matches 1.. at @e[tag=rlk_body,limit=1] run function rlk:items/dbg_poll_i
execute if score @s dbgPage matches 1.. run scoreboard players operation @s dbgPageCur = @s dbgPage
execute if score @s dbgPage matches 1.. at @s run function rlk:items/debug_show
execute if score @s dbgPage matches 1.. run scoreboard players set @s dbgPage 0

# ===== 자기(시스템) 유발 인벤 이벤트 소비 =====
# 이 틱에 우리 코드가 쓴 인벤 변화는 dirty 대상이 아님. 플레이어 클릭/줍기는 다음 틱에 정상 감지됨
scoreboard players set @s invEvt 0
execute store result score @s invCnt if items entity @s inventory.* *[minecraft:custom_data~{rlk:{}}]
execute store result score #ic2 tmp if items entity @s hotbar.* *[minecraft:custom_data~{rlk:{}}]
scoreboard players operation @s invCnt += #ic2 tmp

# Apply pose and its hit/audio events after movement, skills and character state.
function rlk:char/motion/tick
