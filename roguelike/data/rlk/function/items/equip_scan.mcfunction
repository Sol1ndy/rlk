# 인벤토리 아이템 스탯 합산 (무거운 파트, @s = 플레이어)
# 인벤 변화(dirty) 시에만 실행. 결과는 eq*(장비 보너스)에 저장, 최종 스탯은 items/stat_light 가 2틱마다 계산
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
scoreboard players set @s eqEnergyRecharge 0
scoreboard players set @s eqPhysBonus 0
scoreboard players set @s eqPyroBonus 0
scoreboard players set @s eqHydroBonus 0
scoreboard players set @s eqElectroBonus 0
scoreboard players set @s eqCryoBonus 0
scoreboard players set @s eqGeoBonus 0
scoreboard players set @s eqAnemoBonus 0
scoreboard players set @s eqDendroBonus 0

# 등록된 모든 아이템 id 를 순회: 보유 개수(it_<id>) 집계 + 개수 × 스탯 합산
# 빠른 길: 방금 인벤 정리(player/inv/manage)가 실물을 order 대로 놓았고 그 밖에 rlk 아이템이 없으면(items/scan_fast) order 의 id 만
# 센다(items/scan_held; 지난 스캔에서 가졌던 id(rlk:scan held)는 0 으로). it_* · eq* 는 전체 순회와 같다
data modify storage rlk:scan hprev set from storage rlk:scan held
data modify storage rlk:scan held set value []
scoreboard players set #scF tmp 0
execute if score #scM tmp matches 1 run function rlk:items/scan_fast
scoreboard players set #scM tmp 0
execute if score #scF tmp matches 1 run function rlk:items/scan_held
execute if score #scF tmp matches 0 run data modify storage rlk:scan ids set from storage rlk:items ids
execute if score #scF tmp matches 0 run function rlk:items/scan_loop
# held 의 주인: 그 사이 다른 플레이어가 스캔했으면(전역 #scEp 가 늘어 있음) 다음 스캔은 전체 순회
scoreboard players add #scEp eqEp 1
scoreboard players operation @s eqEp = #scEp eqEp

# 낡은 석판: 양옆 칸 아이템의 스탯 증가
execute if score @s it_old_slate matches 1.. run function rlk:items/slate/scan

# 각인: 개수 집계 + 2개 효과(스탯)
function rlk:engravings/scan

# 스캔 직후 최종 스탯도 즉시 갱신
function rlk:items/stat_light
