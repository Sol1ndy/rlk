# 개수만큼 스탯 합산 (@s = 플레이어, #cnt ≥ 1). 이 id 를 이번 스캔의 보유 목록에 적음(items/equip_scan 의 빠른 길이 다음에 0 으로 되돌릴 id)
data modify storage rlk:scan held append from storage rlk:scan cur
# 아이템 stats 키: atkPct(공격력 %) atkFlat(공격력 +) hpPct(최대 체력 %) hpFlat(최대 체력 +) defPct(방어력 %) defFlat(방어력 +)
#                  elemMastery critChance critDamage moveSpeed atkSpeed energyRecharge(원소 충전 효율 %)
#                  physBonus(물리 피해 보너스 %) pyroBonus hydroBonus electroBonus cryoBonus geoBonus anemoBonus dendroBonus(원소 피해 보너스 %)
# 강화 단계에 따른 효과량 배율(‰): #cntF = 개수 × 배율 (÷1000, 반올림)
function rlk:items/tune/fac
scoreboard players operation #cntF tmp = #cnt tmp
scoreboard players operation #cntF tmp *= #fA tmp
# 정의에 있는 스탯만 더한다(items/scan_s/<키>: eq<키> += (값 × #cntF + 500) / 1000, 매크로 없음). 없는 스탯은 0 을 더한 것과 같다
execute if data storage rlk:scan def.stats.atkPct run function rlk:items/scan_s/atk_pct
execute if data storage rlk:scan def.stats.atkFlat run function rlk:items/scan_s/atk_flat
execute if data storage rlk:scan def.stats.hpPct run function rlk:items/scan_s/hp_pct
execute if data storage rlk:scan def.stats.hpFlat run function rlk:items/scan_s/hp_flat
execute if data storage rlk:scan def.stats.defPct run function rlk:items/scan_s/def_pct
execute if data storage rlk:scan def.stats.defFlat run function rlk:items/scan_s/def_flat
execute if data storage rlk:scan def.stats.elemMastery run function rlk:items/scan_s/elem_mastery
execute if data storage rlk:scan def.stats.critChance run function rlk:items/scan_s/crit_chance
execute if data storage rlk:scan def.stats.critDamage run function rlk:items/scan_s/crit_damage
execute if data storage rlk:scan def.stats.moveSpeed run function rlk:items/scan_s/move_speed
execute if data storage rlk:scan def.stats.atkSpeed run function rlk:items/scan_s/atk_speed
execute if data storage rlk:scan def.stats.energyRecharge run function rlk:items/scan_s/energy_recharge
execute if data storage rlk:scan def.stats.physBonus run function rlk:items/scan_s/phys_bonus
execute if data storage rlk:scan def.stats.pyroBonus run function rlk:items/scan_s/pyro_bonus
execute if data storage rlk:scan def.stats.hydroBonus run function rlk:items/scan_s/hydro_bonus
execute if data storage rlk:scan def.stats.electroBonus run function rlk:items/scan_s/electro_bonus
execute if data storage rlk:scan def.stats.cryoBonus run function rlk:items/scan_s/cryo_bonus
execute if data storage rlk:scan def.stats.geoBonus run function rlk:items/scan_s/geo_bonus
execute if data storage rlk:scan def.stats.anemoBonus run function rlk:items/scan_s/anemo_bonus
execute if data storage rlk:scan def.stats.dendroBonus run function rlk:items/scan_s/dendro_bonus
# 예전 판(모든 키를 0 으로 채운 매크로, 마지막 키 dendroBonus)이 남기던 #v 와 같게
execute unless data storage rlk:scan def.stats.dendroBonus run scoreboard players set #v tmp 0
