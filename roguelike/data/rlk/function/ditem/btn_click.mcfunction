# @s = 좌클릭된 버튼 (회수 / 판매)
# 방금 UI 를 누른 직후(uiCd)에는 무시
execute if score @a[tag=player,limit=1] uiCd matches 1.. run return run data remove entity @s attack
scoreboard players set #retok tmp 0
execute if entity @s[tag=rlk_dbtnR] run function rlk:ditem/do_retrieve
execute if entity @s[tag=rlk_dbtnS] run function rlk:ditem/do_sell
data remove entity @s attack
