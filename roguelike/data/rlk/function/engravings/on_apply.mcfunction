# 몹이 피해를 받을 때 (@s = 몹). 각인의 '주는 피해 증가'를 모두 더해서 #dmg 에 한 번 곱한다. 반응 피해(#tfm)에는 적용하지 않음
# 월광: 격변 반응 피해 증가 · 치명타
execute if score #tfm tmp matches 1 if score lunar engN matches 2.. if score #dmg tmp matches 1.. run function rlk:engravings/lunar/tfm
execute if score #tfm tmp matches 1 run return 0
# 빙설 4개: 빙결된 적 → 치명타 확률 추가(이 대상에게만 치명타로 바뀔 수 있음)
execute if score frost engN matches 4.. if score #crit tmp matches 0 if score @s frzT matches 1.. run function rlk:engravings/frost/crit
# 해류·금강 4개: 캐릭터가 주는 피해에 최대 체력 / 방어력의 일부를 더한다(아이템 효과 #sub 제외, 치명타면 그만큼 커짐)
execute if score tide engN matches 4.. unless score #sub itv matches 1 if score #dmg tmp matches 1.. run function rlk:engravings/flat {obj:"maxHealth",pm:"#tidePm"}
execute if score vajra engN matches 4.. unless score #sub itv matches 1 if score #dmg tmp matches 1.. run function rlk:engravings/flat {obj:"def",pm:"#vajraPm"}
scoreboard players set #eb eng 0
# 스탯: 이 피해의 원소(0 = 물리)에 맞는 피해 보너스
execute if score #elem tmp matches 0 run scoreboard players operation #eb eng += @a[tag=player,limit=1] physBonus
execute if score #elem tmp matches 1 run scoreboard players operation #eb eng += @a[tag=player,limit=1] pyroBonus
execute if score #elem tmp matches 2 run scoreboard players operation #eb eng += @a[tag=player,limit=1] hydroBonus
execute if score #elem tmp matches 3 run scoreboard players operation #eb eng += @a[tag=player,limit=1] electroBonus
execute if score #elem tmp matches 4 run scoreboard players operation #eb eng += @a[tag=player,limit=1] cryoBonus
execute if score #elem tmp matches 5 run scoreboard players operation #eb eng += @a[tag=player,limit=1] geoBonus
execute if score #elem tmp matches 6 run scoreboard players operation #eb eng += @a[tag=player,limit=1] anemoBonus
execute if score #elem tmp matches 7 run scoreboard players operation #eb eng += @a[tag=player,limit=1] dendroBonus
# 연계: 스킬·폭발 피해 증가 / 스킬·폭발 적중 뒤 기본 공격 피해 증가
execute if score chain engN matches 2.. if score #skillDmg tmp matches 1 run scoreboard players operation #eb eng += #chainSkill tmp
execute if score chain engN matches 4.. run function rlk:engravings/chain/check
# 협동: 아이템 효과로 주는 피해(#sub) 증가 / 적중하면 공격력 증가
execute if score coop engN matches 2.. if score #sub itv matches 1 run scoreboard players operation #eb eng += #coopDmg tmp
execute if score coop engN matches 4.. if score #sub itv matches 1 if score #dmg tmp matches 1.. run scoreboard players operation #coopT eng = #coopDur tmp
# 침식 5개: 원소 반응을 일으킨 적이 받는 피해 증가
execute if score erode engN matches 5.. run function rlk:engravings/erode/check
execute if score guard engN matches 4.. if score @a[tag=player,limit=1] gShield matches 1.. run scoreboard players operation #eb eng += #guardDmg tmp
execute if score unyielding engN matches 4.. if score #lowHp eng matches 1 run scoreboard players operation #eb eng += #unyDmg tmp
execute if score execute engN matches 4.. run function rlk:engravings/execute/check
execute if score berserk engN matches 4.. run scoreboard players operation #eb eng += #berDmg tmp
# 계약 4개: 생명의 계약 해소 뒤 주는 피해 증가
execute if score pact engN matches 4.. if score #pactT eng matches 1.. run scoreboard players operation #eb eng += #pactDmg tmp
# 아이템의 주는 피해 증가도 여기에 더한다
function rlk:items/hook/dmg_bonus
execute unless score #eb eng matches 1.. run return 0
scoreboard players add #eb eng 100
scoreboard players operation #dmg tmp *= #eb eng
scoreboard players operation #dmg tmp /= #100 tmp
