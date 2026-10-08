# @s = 플레이어. 현재 체력의 #gringCost% 를 잃고(1 아래로는 내려가지 않음) 풀고리 시작
scoreboard players operation #t1 itv = @s curHealth
scoreboard players operation #t1 itv *= #gringCost tmp
scoreboard players operation #t1 itv /= #100 tmp
scoreboard players operation @s curHealth -= #t1 itv
execute if score @s curHealth matches ..0 run scoreboard players set @s curHealth 1
scoreboard players operation #gringT itv = #gringDur tmp
playsound minecraft:block.azalea_leaves.place master @a ~ ~ ~ 1 0.8
