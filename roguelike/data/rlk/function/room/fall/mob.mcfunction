# 몹이 낙사 구간에 떨어짐 (@s = 몹): 즉사. 경험치·골드·회복 구슬은 플레이어의 안전한 자리에 나온다. 보스는 죽지 않고 그 자리로 올라온다
execute if entity @s[tag=boss] at @e[tag=rlk_safe,limit=1] run return run tp @s ~ ~ ~
scoreboard players set #mobKilled tmp 1
scoreboard players set #killBoss tmp 0
scoreboard players set #killMini tmp 0
execute if entity @s[tag=miniboss] run scoreboard players set #killMini tmp 1
execute at @e[tag=rlk_safe,limit=1] run function rlk:room/fall/mob_reward
execute at @s unless score #k13 snd matches 1 run function rlk:snd/f13
kill @s
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:combat/on_kill
