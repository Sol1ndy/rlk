# 누락 스탯을 0으로 채운 뒤 개수만큼 합산 (@s = 플레이어)
# 아이템 stats 키: atkPct(공격력 %) atkFlat(공격력 +) hpPct(최대 체력 %) hpFlat(최대 체력 +) defPct(방어력 %) defFlat(방어력 +)
#                  elemMastery critChance critDamage moveSpeed atkSpeed energyRecharge(원소 충전 효율 %)
#                  physBonus(물리 피해 보너스 %) pyroBonus hydroBonus electroBonus cryoBonus geoBonus anemoBonus dendroBonus(원소 피해 보너스 %)
data modify storage rlk:scan s set value {atkPct:0,atkFlat:0,hpPct:0,hpFlat:0,defPct:0,defFlat:0,elemMastery:0,critChance:0,critDamage:0,moveSpeed:0,atkSpeed:0,energyRecharge:0,physBonus:0,pyroBonus:0,hydroBonus:0,electroBonus:0,cryoBonus:0,geoBonus:0,anemoBonus:0,dendroBonus:0}
data modify storage rlk:scan s merge from storage rlk:scan def.stats
# 강화 단계에 따른 효과량 배율(‰): #cntF = 개수 × 배율 (scan_add 가 ÷1000, 반올림)
function rlk:items/tune/fac
scoreboard players operation #cntF tmp = #cnt tmp
scoreboard players operation #cntF tmp *= #fA tmp
function rlk:items/scan_add with storage rlk:scan s
