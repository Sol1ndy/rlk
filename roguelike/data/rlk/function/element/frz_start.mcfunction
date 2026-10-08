# @s 를 #frzTicks 틱 동안 빙결. boss 태그는 면역, 플레이어는 최대 2초
execute if entity @s[tag=boss] run return 0
execute if entity @s[type=minecraft:player] if score #frzTicks tmp matches 41.. run scoreboard players set #frzTicks tmp 40
execute unless score @s frzT matches 1.. run function rlk:element/frz_on
execute unless score @s frzT >= #frzTicks tmp run scoreboard players operation @s frzT = #frzTicks tmp
