# 각인 매 틱 (@s = 플레이어)
# 정보 아이템이 제자리에 없으면 다시 만든다
execute unless items entity @s inventory.7 *[minecraft:custom_data~{rlk_eng:1b}] unless score @s devMode matches 1 run function rlk:engravings/info_build
# 각인 아이템을 집어 옮겼으면 다시 놓는다(커서에 든 것 = 인벤토리 밖의 사본이 생김)
execute unless score @s devMode matches 1 store result score #t1 eng run clear @s *[minecraft:custom_data~{rlk_engi:1b}] 0
execute unless score @s devMode matches 1 unless score #t1 eng = @s engItems run function rlk:engravings/info_fix
# 불굴: 체력이 낮은지 (현재 체력 × 100 < 최대 체력 × #unyHp)
scoreboard players set #lowHp eng 0
scoreboard players operation #t1 eng = @s curHealth
scoreboard players operation #t1 eng *= #100 tmp
scoreboard players operation #t2 eng = @s maxHealth
scoreboard players operation #t2 eng *= #unyHp tmp
execute if score #t1 eng < #t2 eng run scoreboard players set #lowHp eng 1
# 타이머: 예리(확정 치명타 쿨타임) · 뇌명(내부 쿨타임) · 반석(원소 피해 증가) · 광전사(공격 속도)
execute if score @s keenCd matches 1.. run scoreboard players remove @s keenCd 1
execute if score #thunderT eng matches 1.. run scoreboard players remove #thunderT eng 1
execute if score #petraT eng matches 1.. run scoreboard players remove #petraT eng 1
execute if score @s berT matches 1.. run scoreboard players remove @s berT 1
# 연계 · 협동 · 전의
execute if score #chainT eng matches 1.. run scoreboard players remove #chainT eng 1
execute if score #coopT eng matches 1.. run scoreboard players remove #coopT eng 1
execute if score #spiritT eng matches 1.. run scoreboard players remove #spiritT eng 1
execute if score #pactT eng matches 1.. run scoreboard players remove #pactT eng 1
execute if score #fmT eng matches 1.. run scoreboard players remove #fmT eng 1
# 수호: 보호막
execute if score guard engN matches 4.. run function rlk:engravings/guard/tick
execute unless score guard engN matches 4.. run function rlk:engravings/guard/off
# 원소: 심연의 원소 스택 표시 + 탄환 발사
execute if score elemental engN matches 4.. if score #abStack eng matches 1.. run scoreboard players operation 심연의원소 stacks = #abStack eng
execute if score elemental engN matches 4.. if score #abStack eng matches 1.. run scoreboard players display name 심연의원소 stacks {text:"심연의 원소",color:"#B58BE8"}
execute unless score #abStack eng matches 1.. run scoreboard players reset 심연의원소 stacks
execute unless score elemental engN matches 4.. run function rlk:engravings/abyss/off
execute if score #aqN eng matches 1.. at @e[tag=rlk_body,limit=1] run function rlk:engravings/abyss/fire
