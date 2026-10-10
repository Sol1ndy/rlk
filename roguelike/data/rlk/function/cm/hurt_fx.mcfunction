# 피격 연출: 붉은 번쩍임 + 소리 (@s = 몸)
execute if entity @s[type=!minecraft:player] run data merge entity @s {InvulnerableTime:0s,HurtTime:0s}
damage @s 0 minecraft:generic
execute unless score #k77 snd matches 1 run function rlk:snd/f83
