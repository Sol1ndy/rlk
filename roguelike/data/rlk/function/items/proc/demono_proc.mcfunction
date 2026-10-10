# @s = 플레이어, at @s. 데모노미콘 발동: 3개 마법 중 하나를 10초간 활성화
scoreboard players set @s bookPages 0
scoreboard players set @s demonoBuff 200
execute store result score @s demonoType run random value 1..3
particle minecraft:witch ~ ~1 ~ 1 1.2 1 0.3 60
particle minecraft:enchant ~ ~2 ~ 1 1 1 1 40
execute unless score #k128 snd matches 1 run function rlk:snd/f136
execute unless score #k129 snd matches 1 run function rlk:snd/f137
execute if score @s demonoType matches 1 run title @s actionbar {"text":"데모노미콘: 심연의 촉수","color":"aqua"}
execute if score @s demonoType matches 2 run title @s actionbar {"text":"데모노미콘: 지옥의 불기둥","color":"aqua"}
execute if score @s demonoType matches 3 run title @s actionbar {"text":"데모노미콘: 서리 화살","color":"aqua"}
# 액션바 HUD 잠시 멈춤(이 안내가 보이도록)
scoreboard players operation @s hudHold = #hudHoldT tmp
