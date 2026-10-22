# @s = 구매하려는 플레이어. 골드 확인 후 구매/거절
execute unless score @s gold matches 0.. run scoreboard players set @s gold 0
execute if score @s gold >= #buyprice tmp run return run function rlk:shop/do_buy
function rlk:shop/deny
