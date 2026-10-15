# 플레이어 초기화 (@s = 플레이어)
# 바닐라 체력은 1024(상한) 고정: 피격 감지용이고 화면의 하트는 리소스팩으로 가린다. 실제 체력은 curHealth / maxHealth
attribute @s minecraft:max_health base set 1024
scoreboard players set @s vhp 1024
attribute @s minecraft:movement_speed base set 0.1
attribute @s minecraft:attack_speed base set 4
# 공격력: 실제 데미지는 전투 시스템이 담당 -> 바닐라는 트리거용 최소값
attribute @s minecraft:attack_damage base set 0.01
attribute @s minecraft:armor base set 0

# 레벨 (기초 체력·공격력·방어력은 레벨에서 계산: player/level/apply)
scoreboard players set @s level 1
scoreboard players set @s xp 0
# 그 밖의 기본(base) 스탯
scoreboard players set @s base_elemMastery 0
scoreboard players set @s base_moveSpeed 100
scoreboard players set @s base_atkSpeed 100
scoreboard players set @s base_critChance 10
scoreboard players set @s base_critDamage 150
# 장비 보너스(인벤 스캔 전 안전값)
scoreboard players set @s eqAtkPct 0
scoreboard players set @s eqAtkFlat 0
scoreboard players set @s eqHpPct 0
scoreboard players set @s eqHpFlat 0
scoreboard players set @s eqDefPct 0
scoreboard players set @s eqDefFlat 0
scoreboard players set @s eqElemMastery 0
scoreboard players set @s eqCritChance 0
scoreboard players set @s eqCritDamage 0
scoreboard players set @s eqMoveSpeed 0
scoreboard players set @s eqAtkSpeed 0

# 자원: 골드는 새로 시작할 때만 0, 사파이어는 리셋해도 유지
execute unless score @s gold matches 0.. run scoreboard players set @s gold 0
execute unless score @s sapphire matches 0.. run scoreboard players set @s sapphire 0
execute unless score @s invCap matches 9..18 run scoreboard players set @s invCap 9

# 내부값
scoreboard players set @s atkCD 0
scoreboard players set @s devMode 0
scoreboard players set @s comboStep 0
scoreboard players set @s cboIdle 0
scoreboard players set @s dead 0
execute unless score @s pid matches 1.. run function rlk:player/assign_pid
# 대쉬(충전식)
scoreboard players operation @s dashCharge = #dashMax tmp
scoreboard players set @s dashRegen 0
scoreboard players set @s dashCool 0
scoreboard players set @s dashInvT 0
scoreboard players set @s dashMoveT 0
scoreboard players set @s hudKey -1
scoreboard players set @s hpKey -1
# 원소
scoreboard players set @s infuse 0
scoreboard players set @s infuseT 0
scoreboard players set @s hurtElem 0
scoreboard players set @s shieldHP 0
scoreboard players set @s shieldT 0
function rlk:element/clear
scoreboard players set @s hudHold 0
# 캐릭터
function rlk:char/player_init
# 인벤 감시
scoreboard players set @s invDirty 2
scoreboard players set @s invEvt 0
scoreboard players set @s invCnt 0
scoreboard players set @s manageTick 0
scoreboard players set @s scanTick 0
scoreboard players set @s uiHash -99999
scoreboard players set @s init 1
# 최종 스탯 계산 + 체력 완충
function rlk:items/stat_light
scoreboard players operation @s curHealth = @s maxHealth
scoreboard players operation @s hpMaxPrev = @s maxHealth
effect give @s minecraft:instant_health 1 20 true
# 자동 초기화 안 되는 아이템 스택 초기화
function rlk:player/reset_stacks
scoreboard players set @s shieldEl 0
