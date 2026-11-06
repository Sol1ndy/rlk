# @s = 플레이어. 인벤 가득
title @s actionbar [{"text":"보유 아이템이 가득 찼습니다 (최대 ","color":"red"},{"score":{"name":"@s","objective":"invCap"},"color":"red"},{"text":")","color":"red"}]
# 액션바 HUD 잠시 멈춤(이 안내가 보이도록)
scoreboard players operation @s hudHold = #hudHoldT tmp
