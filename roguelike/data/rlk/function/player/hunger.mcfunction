# 허기를 20으로 고정 (@s = 플레이어)
# 플레이어 foodLevel 은 /data 로 직접 못 쓰므로 saturation 효과로 채움
execute store result score #food tmp run data get entity @s foodLevel
execute if score #food tmp matches ..19 run effect give @s minecraft:saturation 1 20 true
