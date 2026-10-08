# @s = 플레이어. 질주 2개: 대쉬 충전 +#dashEngMax 개, 충전 속도 +#dashEngSpd% (충전 시간 = 기본 × 100 / (100 + 속도))
scoreboard players operation #dashMax tmp = #dashMaxBase tmp
scoreboard players operation #dashRegenT tmp = #dashRegenBase tmp
execute if score dash engN matches 2.. run scoreboard players operation #dashMax tmp += #dashEngMax tmp
execute if score dash engN matches 2.. run function rlk:engravings/dash/regen
execute if score @s dashCharge > #dashMax tmp run scoreboard players operation @s dashCharge = #dashMax tmp
scoreboard players set @s hudKey -1
