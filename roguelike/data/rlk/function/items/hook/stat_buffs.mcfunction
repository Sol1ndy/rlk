# 스탯 버프 적용 지점 (@s = 플레이어, 2틱마다 stat_light 에서 호출)
# 공격력·체력·방어력: 누산기에 더한다
#   % 증가  → atkPct / hpPct / defPct      예) execute if score @s xxxBuff matches 1.. run scoreboard players add @s atkPct 20
#   깡 증가 → atkFlat / hpFlat / defFlat   예) execute if score @s xxxBuff matches 1.. run scoreboard players add @s atkFlat 15
#   증폭(×) → ampAtk (100 = ×1)            예) execute if score @s xxxBuff matches 1.. run scoreboard players add @s ampAtk 45
# 그 밖(elemMastery critChance critDamage moveSpeed atkSpeed)은 스탯에 직접 더한다
# 피해 보너스: physBonus pyroBonus hydroBonus electroBonus cryoBonus geoBonus anemoBonus dendroBonus 에 직접 더한다
# 고통 & 절망: 스택당 공격속도 +1.5, 이동속도 +1 (2초 유지)
execute if score @s it_pain_despair matches 1.. if score @s pdT matches 1.. run function rlk:items/proc/pd_apply
# 각인: 보물(가진 골드에 따라 공격력%) · 광전사(처치 뒤 공격 속도)
function rlk:engravings/stat_buffs
# 격려의 깃발: 영역 안에서 공격력 증가
execute if score #flagIn itv matches 1.. run scoreboard players operation @s atkPct += #flagAtk tmp
# 대장의 군기 · 서리달의 은잔 · 특순대 휘장
execute if score #gflagIn itv matches 1.. run scoreboard players operation @s defPct += #gflagDef tmp
execute if score #muskT itv matches 1.. run scoreboard players operation @s atkPct += #muskAtk tmp
# 스칸다의 씨앗(원소폭발 뒤) · 텐구의 깃 · 열혈 저울 · 바람 슬라임 인형
execute if score #mayaT itv matches 1.. run scoreboard players operation @s elemMastery += #mayaEm tmp
execute if score #tenguT itv matches 1.. run scoreboard players operation @s atkPct += #tenguAtk tmp
execute if score #kinT itv matches 1.. run scoreboard players operation @s atkPct += #kinAtk tmp
execute if score #slimeT itv matches 1.. run scoreboard players operation @s elemMastery += #slimeEm tmp
# 원소 피해 보너스: 대장의 군기(바위) · 용의 불씨(불) · 단풍잎 한 장(확산된 원소) · 음원 샘플(모든 원소)
execute if score #gflagIn itv matches 1.. run scoreboard players operation @s geoBonus += #gflagDmg tmp
execute if score #dragT itv matches 1.. run scoreboard players operation @s pyroBonus += #dragFire tmp
execute if score #mapleT itv matches 1.. if score #mapleEl itv matches 1 run scoreboard players operation @s pyroBonus += #mapleDmg tmp
execute if score #mapleT itv matches 1.. if score #mapleEl itv matches 2 run scoreboard players operation @s hydroBonus += #mapleDmg tmp
execute if score #mapleT itv matches 1.. if score #mapleEl itv matches 3 run scoreboard players operation @s electroBonus += #mapleDmg tmp
execute if score #mapleT itv matches 1.. if score #mapleEl itv matches 4 run scoreboard players operation @s cryoBonus += #mapleDmg tmp
execute if score #mapleT itv matches 1.. if score #mapleEl itv matches 5 run scoreboard players operation @s geoBonus += #mapleDmg tmp
execute if score #mapleT itv matches 1.. if score #mapleEl itv matches 6 run scoreboard players operation @s anemoBonus += #mapleDmg tmp
execute if score #mapleT itv matches 1.. if score #mapleEl itv matches 7 run scoreboard players operation @s dendroBonus += #mapleDmg tmp
execute if score #srcN itv matches 3.. run scoreboard players operation @s pyroBonus += #srcDmg tmp
execute if score #srcN itv matches 3.. run scoreboard players operation @s hydroBonus += #srcDmg tmp
execute if score #srcN itv matches 3.. run scoreboard players operation @s electroBonus += #srcDmg tmp
execute if score #srcN itv matches 3.. run scoreboard players operation @s cryoBonus += #srcDmg tmp
execute if score #srcN itv matches 3.. run scoreboard players operation @s geoBonus += #srcDmg tmp
execute if score #srcN itv matches 3.. run scoreboard players operation @s anemoBonus += #srcDmg tmp
execute if score #srcN itv matches 3.. run scoreboard players operation @s dendroBonus += #srcDmg tmp
# 요이미야 고유 특성 소매불 백경도: 스택당 불 원소 피해 보너스
execute if score #charN tmp matches 2 if score @s yoiP matches 1.. run function rlk:char/yoimiya/passive_stat
# 클로린드 고유 특성: 생명의 계약이 변할 때마다 치명타 확률
execute if score #charN tmp matches 4 if score @s clP matches 1.. run function rlk:char/clorinde/passive_stat
# 아를레키노: 붉은 죽음의 가면 중 불 원소 피해 보너스
execute if score #charN tmp matches 5 if score @s arM matches 1 run scoreboard players operation @s pyroBonus += #arPyro tmp
# 아이템(4차): 고양이 꼬리 칵테일 · 죄인의 창끝 · 서약의 단검 · 민들레 씨앗 · 꿈결 베개 · 달빛 베틀
execute if score @s it_cat_cocktail matches 1.. run function rlk:items/proc/cocktail
execute if score #sinT itv matches 1.. run scoreboard players operation @s critChance += #sinCrit tmp
execute if score @s it_pact_dagger matches 1.. if score @s bol matches 1.. run scoreboard players operation @s atkSpeed += #daggerSpd tmp
execute if score #dandT itv matches 1.. run scoreboard players operation @s moveSpeed += #dandSpd tmp
execute if score #pillowT itv matches 1.. run scoreboard players operation @s elemMastery += #pillowEm tmp
execute if score #pillowT itv matches 1.. run scoreboard players operation @s moveSpeed += #pillowSpd tmp
execute if score #loomT itv matches 1.. run scoreboard players operation @s elemMastery += #loomEm tmp
# 네페르: 기본 원소 마스터리 +#nfEm, 기만의 장막 3스택 = +100
execute if score #charN tmp matches 8 run scoreboard players operation @s elemMastery += #nfEm tmp
execute if score #charN tmp matches 8 if score @s nfVeil matches 3.. run scoreboard players add @s elemMastery 100
# 중간보스 전투 중 치명타 확률 보정(#mbCritAdd: 달빛 고치 −100, 달빛 축복 받음 +15). 전투가 끝나면 0
execute if score #mbLive mb matches 1 run scoreboard players operation @s critChance += #mbCritAdd mb
