# @s = 플레이어, at @s anchored eyes. 좌클릭(공격)으로 상점 구매/리롤 (atkBlock 우회)
# 별도 레이캐스트 대신 "호버된(글씨 커진) 버튼"을 그대로 사용 → 확대 기준과 구매 기준이 항상 동일
scoreboard players set #shopHandled tmp 0
execute as @e[tag=rlk_shop_btn,tag=rlk_shop_hover,limit=1,sort=nearest] at @s run function rlk:shop/ray_buy
execute if score #shopHandled tmp matches 0 as @e[tag=rlk_shop_reroll,tag=rlk_shop_hover,limit=1,sort=nearest] at @s run function rlk:shop/ray_reroll
