# 최종 스탯 계산 (@s = 플레이어, 2틱마다)
#   공격력 = 기초 공격력 × (100 + 공격력%) / 100 + 깡 공격력   (그 뒤 증폭 ampAtk% 곱)
#   최대 체력 = 기초 체력 × (100 + 체력%) / 100 + 깡 체력
#   방어력 = 기초 방어력 × (100 + 방어력%) / 100 + 깡 방어력
# 기초(base_*) 값은 레벨에서 나온다(player/level/apply). 나머지 스탯은 기본(base) + 장비(eq)
scoreboard players set @s scanTick 2
function rlk:player/level/apply
# 장비 보너스 → 작업용 누산기 (버프는 items/hook/stat_buffs 에서 여기에 더한다)
scoreboard players operation @s atkPct = @s eqAtkPct
scoreboard players operation @s atkFlat = @s eqAtkFlat
scoreboard players operation @s hpPct = @s eqHpPct
scoreboard players operation @s hpFlat = @s eqHpFlat
scoreboard players operation @s defPct = @s eqDefPct
scoreboard players operation @s defFlat = @s eqDefFlat
scoreboard players operation @s elemMastery = @s base_elemMastery
scoreboard players operation @s elemMastery += @s eqElemMastery
scoreboard players operation @s critChance = @s base_critChance
scoreboard players operation @s critChance += @s eqCritChance
scoreboard players operation @s critDamage = @s base_critDamage
scoreboard players operation @s critDamage += @s eqCritDamage
scoreboard players operation @s moveSpeed = @s base_moveSpeed
scoreboard players operation @s moveSpeed += @s eqMoveSpeed
scoreboard players operation @s atkSpeed = @s base_atkSpeed
scoreboard players operation @s atkSpeed += @s eqAtkSpeed
scoreboard players operation @s energyRecharge = @s base_energyRecharge
scoreboard players operation @s energyRecharge += @s eqEnergyRecharge
# 피해 보너스(물리·원소별): 기본 0 + 장비. 버프는 stat_buffs 에서 더한다
scoreboard players operation @s physBonus = @s eqPhysBonus
scoreboard players operation @s pyroBonus = @s eqPyroBonus
scoreboard players operation @s hydroBonus = @s eqHydroBonus
scoreboard players operation @s electroBonus = @s eqElectroBonus
scoreboard players operation @s cryoBonus = @s eqCryoBonus
scoreboard players operation @s geoBonus = @s eqGeoBonus
scoreboard players operation @s anemoBonus = @s eqAnemoBonus
scoreboard players operation @s dendroBonus = @s eqDendroBonus
# 증폭(곱연산) 누산기 초기화 (100 = ×1.00)
scoreboard players set @s ampAtk 100
function rlk:items/hook/stat_buffs
# ===== 최종값 =====
scoreboard players operation @s atk = @s atkPct
scoreboard players add @s atk 100
scoreboard players operation @s atk *= @s base_atk
scoreboard players operation @s atk /= #100 tmp
scoreboard players operation @s atk += @s atkFlat
scoreboard players operation @s atk *= @s ampAtk
scoreboard players operation @s atk /= #100 tmp
execute if score @s atk matches ..0 run scoreboard players set @s atk 1
scoreboard players operation @s maxHealth = @s hpPct
scoreboard players add @s maxHealth 100
scoreboard players operation @s maxHealth *= @s base_maxHealth
scoreboard players operation @s maxHealth /= #100 tmp
scoreboard players operation @s maxHealth += @s hpFlat
execute if score @s maxHealth matches ..0 run scoreboard players set @s maxHealth 1
scoreboard players operation @s def = @s defPct
scoreboard players add @s def 100
scoreboard players operation @s def *= @s base_def
scoreboard players operation @s def /= #100 tmp
scoreboard players operation @s def += @s defFlat
execute if score @s def matches ..-1 run scoreboard players set @s def 0
# 최대 체력이 바뀌면 현재 체력을 같은 비율로 맞춤
execute unless score @s maxHealth = @s hpMaxPrev run function rlk:player/hp_scale
