# 각인 개수 집계 (@s = 플레이어, items/equip_scan 에서 호출 = 인벤이 바뀔 때만). 결과: <각인 id> engN = 개수
scoreboard players reset * engN
data modify storage rlk:lvpick iq set from storage rlk:pinv order
data modify storage rlk:lvpick a.obj set value "engN"
function rlk:engravings/scan_loop
# 시험용 추가 개수(engravings/dev)
execute if score guard engDev matches 1.. run scoreboard players operation guard engN += guard engDev
execute if score elemental engDev matches 1.. run scoreboard players operation elemental engN += elemental engDev
execute if score unyielding engDev matches 1.. run scoreboard players operation unyielding engN += unyielding engDev
execute if score amplify engDev matches 1.. run scoreboard players operation amplify engN += amplify engDev
execute if score emblem engDev matches 1.. run scoreboard players operation emblem engN += emblem engDev
execute if score cycle engDev matches 1.. run scoreboard players operation cycle engN += cycle engDev
execute if score keen engDev matches 1.. run scoreboard players operation keen engN += keen engDev
execute if score dash engDev matches 1.. run scoreboard players operation dash engN += dash engDev
execute if score frost engDev matches 1.. run scoreboard players operation frost engN += frost engDev
execute if score execute engDev matches 1.. run scoreboard players operation execute engN += execute engDev
execute if score treasure engDev matches 1.. run scoreboard players operation treasure engN += treasure engDev
execute if score flurry engDev matches 1.. run scoreboard players operation flurry engN += flurry engDev
execute if score thunder engDev matches 1.. run scoreboard players operation thunder engN += thunder engDev
execute if score petra engDev matches 1.. run scoreboard players operation petra engN += petra engDev
execute if score berserk engDev matches 1.. run scoreboard players operation berserk engN += berserk engDev
execute if score tide engDev matches 1.. run scoreboard players operation tide engN += tide engDev
execute if score vajra engDev matches 1.. run scoreboard players operation vajra engN += vajra engDev
execute if score chain engDev matches 1.. run scoreboard players operation chain engN += chain engDev
execute if score erode engDev matches 1.. run scoreboard players operation erode engN += erode engDev
execute if score lunar engDev matches 1.. run scoreboard players operation lunar engN += lunar engDev
execute if score coop engDev matches 1.. run scoreboard players operation coop engN += coop engDev
execute if score spirit engDev matches 1.. run scoreboard players operation spirit engN += spirit engDev
execute if score pact engDev matches 1.. run scoreboard players operation pact engN += pact engDev
execute if score fullmoon engDev matches 1.. run scoreboard players operation fullmoon engN += fullmoon engDev
# 세계수의 기적(나무뿌리 노드): 고른 각인 개수 +1
execute if data storage rlk:pinv mir run function rlk:engravings/mir_add with storage rlk:pinv
# 개수 효과: 스탯 (장비 보너스 eq* 에 더함)
execute if score guard engN matches 2.. run scoreboard players operation @s eqDefPct += #es_guard2 tmp
execute if score elemental engN matches 2.. run scoreboard players operation @s eqAtkPct += #es_elemental2 tmp
execute if score unyielding engN matches 2.. run scoreboard players operation @s eqDefPct += #es_unyielding2 tmp
execute if score amplify engN matches 2.. run scoreboard players operation @s eqElemMastery += #es_amplify2 tmp
execute if score emblem engN matches 2.. run scoreboard players operation @s eqEnergyRecharge += #es_emblem2 tmp
execute if score frost engN matches 2.. run scoreboard players operation @s eqCryoBonus += #frostDmg tmp
execute if score keen engN matches 2.. run scoreboard players operation @s eqCritChance += #es_keen2 tmp
execute if score keen engN matches 4.. run scoreboard players operation @s eqCritDamage += #es_keen4 tmp
execute if score dash engN matches 1.. run scoreboard players operation @s eqMoveSpeed += #es_dash1 tmp
execute if score execute engN matches 2.. run scoreboard players operation @s eqAtkPct += #es_execute2 tmp
execute if score flurry engN matches 2.. run scoreboard players operation @s eqAtkSpeed += #es_flurry2 tmp
execute if score berserk engN matches 2.. run scoreboard players operation @s eqAtkPct += #es_berserk2 tmp
execute if score tide engN matches 2.. run scoreboard players operation @s eqHpPct += #es_tide2 tmp
execute if score vajra engN matches 2.. run scoreboard players operation @s eqDefPct += #es_vajra2 tmp
execute if score erode engN matches 2.. run scoreboard players operation @s eqElemMastery += #es_erode2 tmp
# 그 밖에 개수에 따라 바뀌는 값(대쉬 충전 등)
function rlk:engravings/scan_more
# 각인 정보 아이템 새로 만들기
function rlk:engravings/info_build
