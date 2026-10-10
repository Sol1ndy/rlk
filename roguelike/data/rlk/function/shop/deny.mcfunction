# @s = 플레이어. 골드 부족
title @s actionbar {"text":"골드가 부족합니다","color":"red"}
execute unless score #k198 snd matches 1 run function rlk:snd/f214
execute unless score #k199 snd matches 1 run function rlk:snd/f215
execute unless score #k200 snd matches 1 run function rlk:snd/f216
# 액션바 HUD 잠시 멈춤(이 안내가 보이도록)
scoreboard players operation @s hudHold = #hudHoldT tmp
