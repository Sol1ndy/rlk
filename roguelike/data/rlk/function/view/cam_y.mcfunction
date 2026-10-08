# 카메라 높이 계산 (@s = 플레이어) → storage rlk:view pr.cy = 카메라가 기준으로 삼을 아바타 머리 높이(절대 좌표)
#   #cby = 기준 바닥 높이(×1000), #avY = 아바타 발 높이(×1000)
execute store result score #avY view run data get entity @e[tag=rlk_av,limit=1] Pos[1] 1000
scoreboard players set #onG view 0
execute as @e[tag=rlk_av,limit=1] if data entity @s {OnGround:1b} run scoreboard players set #onG view 1
execute unless score #cby view = #cby view run scoreboard players operation #cby view = #avY view
scoreboard players operation #cd view = #avY view
scoreboard players operation #cd view -= #cby view
# 순간이동 등으로 많이 벌어졌으면 바로 맞춤
execute if score #cd view matches 3000.. run scoreboard players operation #cby view = #avY view
execute if score #cd view matches ..-3000 run scoreboard players operation #cby view = #avY view
# 기준보다 아래로 내려가면(낙하) 그대로 따라감
execute if score #cd view matches ..-1 run scoreboard players operation #cby view = #avY view
# 땅에 서 있는데 기준보다 높으면(턱·계단을 올라섬) 틱당 0.25칸씩 따라감
execute if score #onG view matches 1 if score #cd view matches 1..250 run scoreboard players operation #cby view = #avY view
execute if score #onG view matches 1 if score #cd view matches 251..2999 run scoreboard players add #cby view 250
# 뛰어오른 높이는 #viewJump% 만 반영
scoreboard players operation #cd view = #avY view
scoreboard players operation #cd view -= #cby view
execute if score #cd view matches ..-1 run scoreboard players set #cd view 0
scoreboard players operation #cd view *= #viewJump tmp
scoreboard players operation #cd view /= #100 tmp
scoreboard players operation #cd view += #cby view
scoreboard players add #cd view 1500
execute store result storage rlk:view pr.cy double 0.001 run scoreboard players get #cd view
