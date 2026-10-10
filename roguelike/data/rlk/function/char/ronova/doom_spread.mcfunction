# 사형 선고를 받은 적이 죽은 자리 (@s = 표시 마커): 근처 6칸 적에게 잠식(죽은 적의 절반) + 공허 부착
scoreboard players operation #g tmp = @s rnEr
execute if score #g tmp matches 1.. as @e[tag=rlk_mob,distance=..6] at @s run function rlk:element/void/gain
execute if score #g tmp matches 1.. as @e[tag=rlk_mob,distance=..6] at @s run particle minecraft:dust{color:[0.88,0.12,0.22],scale:1.2} ~ ~1.2 ~ 0.2 0.4 0.2 0 10
particle minecraft:reverse_portal ~ ~ ~ 1.5 0.5 1.5 0.2 30
execute unless score #k275 snd matches 1 run function rlk:snd/f310
kill @s
