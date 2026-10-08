# @s = 플레이어, at @s (매 틱, demonoBuff>0). 20틱마다 활성 마법 1회 발동
scoreboard players remove @s demonoBuff 1
scoreboard players operation #dm tmp = @s demonoBuff
scoreboard players operation #dm tmp %= #st20 tmp
execute if score #dm tmp matches 0 if score @s demonoType matches 1 run function rlk:items/proc/demono_tentacle
execute if score #dm tmp matches 0 if score @s demonoType matches 2 run function rlk:items/proc/demono_pillar
execute if score #dm tmp matches 0 if score @s demonoType matches 3 run function rlk:items/proc/demono_fireball
