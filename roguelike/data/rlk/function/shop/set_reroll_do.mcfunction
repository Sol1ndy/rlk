# at = 블록 코너. 리롤 좌표 저장 + (x,y+0.5,z)에 텍스트+인터랙션
kill @e[tag=rlk_shop_reroll,distance=..2]
kill @e[tag=rlk_shop_rlbl,distance=..2]
data modify storage rlk:shop rcost set from storage rlk:shop reroll_cost
function rlk:shop/spawn_reroll with storage rlk:shop
tellraw @a[distance=..0.01] {"text":"[상점] 리롤 버튼 설정됨","color":"aqua"}
