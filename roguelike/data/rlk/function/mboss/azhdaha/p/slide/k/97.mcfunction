# slide #azPT 97
execute at @s rotated as @s rotated ~ 0 positioned ^0 ^0 ^2.4 run execute if score #azE mb matches 1 run function rlk:mboss/azhdaha/fx/p/impact/1
execute at @s rotated as @s rotated ~ 0 positioned ^0 ^0 ^2.4 run execute if score #azE mb matches 2 run function rlk:mboss/azhdaha/fx/p/impact/2
execute at @s rotated as @s rotated ~ 0 positioned ^0 ^0 ^2.4 run execute if score #azE mb matches 3 run function rlk:mboss/azhdaha/fx/p/impact/3
execute at @s rotated as @s rotated ~ 0 positioned ^0 ^0 ^2.4 run execute if score #azE mb matches 4 run function rlk:mboss/azhdaha/fx/p/impact/4
execute at @s rotated as @s rotated ~ 0 positioned ^0 ^0 ^2.4 run execute if score #azE mb matches 5 run function rlk:mboss/azhdaha/fx/p/impact/5
function rlk:mboss/azhdaha/fx/snd/slide_wave
function rlk:mboss/grp_new
kill @e[type=minecraft:marker,tag=rlk_mb_az_p20w2]
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzAct mb 6
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNoDodge mb 1
scoreboard players set #hzNR mb 1
scoreboard players set #hzY1 mb 7
scoreboard players operation #hzEl mb = #azE mb
scoreboard players operation #pjEl mb = #azE mb
function rlk:mboss/hz/ring {r0:0,r:40,tell:20,dmg:80}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p20w2
scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_p20w2,limit=1] mb 3000
execute if score #azTrN mb matches ..1 run function rlk:mboss/line/say {t:"천 년의 원한을 어찌 갚을까!",c:"#F2B53A",gap:2,hold:50,snd:2}
execute if score #azTrN mb matches 2 run function rlk:mboss/line/say {t:"오늘이야말로 묵은 원한을 전부 청산하지!",c:"#F2B53A",gap:2,hold:50,snd:2}
