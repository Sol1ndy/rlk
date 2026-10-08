# @s = 피해를 받는 몹, at @s. 유금화광이 붙어 있고 요이미야의 일반 공격·조준 사격(아이템 효과·반응 피해·원소폭발·유금화광 폭발 자신은 제외)에 맞으면 폭발을 예약한다(쿨타임 #yoiBoomCdT)
execute if score #tfm tmp matches 1 run return 0
execute if score #sub itv matches 1 run return 0
execute if score #yoiBoom tmp matches 1 run return 0
execute if score #yoiBoomCd tmp matches 1.. run return 0
execute store result score #ynow tmp run time query gametime
execute unless score @s aurEnd > #ynow tmp run return 0
scoreboard players operation #yoiBoomCd tmp = #yoiBoomCdT tmp
summon minecraft:marker ~ ~ ~ {Tags:["rlk_iq","rlk_iqn"]}
scoreboard players set @e[tag=rlk_iqn] iqK 4
tag @e[tag=rlk_iqn] remove rlk_iqn
