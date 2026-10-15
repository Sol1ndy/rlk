# macro: 옆 아이템의 stats (slate/boost, 옆 아이템 id = rlk:scan b.id). 더하는 값 = 스탯 × #slatePct% × 옆 아이템의 강화 배율(#fA ‰)
# #slF = #slatePct × #fA ÷ 10 → 스탯 × #slF ÷ 10000 (옆 아이템이 3단계면 스탯 × #slatePct ÷ 100 그대로)
scoreboard players set #enh tmp 0
function rlk:items/enh_get with storage rlk:scan b
function rlk:items/tune/fac
scoreboard players operation #slF tmp = #slatePct tmp
scoreboard players operation #slF tmp *= #fA tmp
scoreboard players operation #slF tmp /= #10 tmp
$scoreboard players set #v tmp $(atkPct)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqAtkPct += #v tmp
$scoreboard players set #v tmp $(atkFlat)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqAtkFlat += #v tmp
$scoreboard players set #v tmp $(hpPct)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqHpPct += #v tmp
$scoreboard players set #v tmp $(hpFlat)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqHpFlat += #v tmp
$scoreboard players set #v tmp $(defPct)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqDefPct += #v tmp
$scoreboard players set #v tmp $(defFlat)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqDefFlat += #v tmp
$scoreboard players set #v tmp $(elemMastery)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqElemMastery += #v tmp
$scoreboard players set #v tmp $(critChance)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqCritChance += #v tmp
$scoreboard players set #v tmp $(critDamage)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqCritDamage += #v tmp
$scoreboard players set #v tmp $(moveSpeed)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqMoveSpeed += #v tmp
$scoreboard players set #v tmp $(atkSpeed)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqAtkSpeed += #v tmp
$scoreboard players set #v tmp $(energyRecharge)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqEnergyRecharge += #v tmp
$scoreboard players set #v tmp $(physBonus)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqPhysBonus += #v tmp
$scoreboard players set #v tmp $(pyroBonus)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqPyroBonus += #v tmp
$scoreboard players set #v tmp $(hydroBonus)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqHydroBonus += #v tmp
$scoreboard players set #v tmp $(electroBonus)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqElectroBonus += #v tmp
$scoreboard players set #v tmp $(cryoBonus)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqCryoBonus += #v tmp
$scoreboard players set #v tmp $(geoBonus)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqGeoBonus += #v tmp
$scoreboard players set #v tmp $(anemoBonus)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqAnemoBonus += #v tmp
$scoreboard players set #v tmp $(dendroBonus)
scoreboard players operation #v tmp *= #slF tmp
scoreboard players operation #v tmp /= #10000 tmp
scoreboard players operation @s eqDendroBonus += #v tmp
