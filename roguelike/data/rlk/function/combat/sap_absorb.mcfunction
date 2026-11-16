# @s = 사파이어 조각. 사파이어 +gval
scoreboard players operation @a[tag=player,limit=1] sapphire += @s gval
# 연출 카메라에 잡혀 있는 동안(mboss/cam/hold, 태그 rlk_mb_camh)에는 채팅 줄을 띄우지 않고 #mbCamSap mb 에 모았다가 풀릴 때 한 번에 알린다(mboss/cam/release)
execute if entity @a[tag=player,tag=rlk_mb_camh] run scoreboard players operation #mbCamSap mb += @s gval
execute unless entity @a[tag=player,tag=rlk_mb_camh] run tellraw @a[tag=player] [{"text":"◇ ","color":"#5B9BF0"},{"text":"사파이어 +","color":"#5B9BF0"},{"score":{"name":"@s","objective":"gval"},"color":"#5B9BF0"}]
execute as @a[tag=player,limit=1] at @s unless score #k28 snd matches 1 run function rlk:snd/f28
execute as @a[tag=player,limit=1] at @s unless score #k18 snd matches 1 run function rlk:snd/f29
kill @s
