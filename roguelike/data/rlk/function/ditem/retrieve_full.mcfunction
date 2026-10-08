# 인벤 가득 (9개) - 회수 불가
playsound minecraft:block.note_block.bass master @s ~ ~ ~ 0.8 0.6
title @s actionbar {"text":"보유 아이템이 가득 찼습니다 (최대 9)","color":"red"}
# 액션바 HUD 잠시 멈춤(이 안내가 보이도록)
scoreboard players operation @s hudHold = #hudHoldT tmp
