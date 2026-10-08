# @s = 플레이어. 골드 부족
title @s actionbar {"text":"골드가 부족합니다","color":"red"}
playsound minecraft:block.note_block.bass master @s ~ ~ ~ 0.6 0.6
playsound minecraft:entity.enderman.teleport master @s ~ ~ ~ 0.8 0.8
playsound minecraft:block.note_block.didgeridoo master @s ~ ~ ~ 0.5 0.5
# 액션바 HUD 잠시 멈춤(이 안내가 보이도록)
scoreboard players operation @s hudHold = #hudHoldT tmp
