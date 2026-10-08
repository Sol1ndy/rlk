# 플레이어가 낙사 구간에 떨어짐 (@s = 플레이어): 최대 체력의 #fallPct% 피해(체력 1 아래로는 내려가지 않음) → 떨어지기 전 자리로
scoreboard players operation #t1 tmp = @s maxHealth
scoreboard players operation #t1 tmp *= #fallPct tmp
scoreboard players operation #t1 tmp /= #100 tmp
execute if score #t1 tmp matches ..0 run scoreboard players set #t1 tmp 1
scoreboard players operation @s curHealth -= #t1 tmp
execute if score @s curHealth matches ..0 run scoreboard players set @s curHealth 1
scoreboard players set @s dashMoveT 0
scoreboard players set @s stepT 0
execute if score @s bowT matches 1.. run function rlk:char/bow/cancel
execute at @e[tag=rlk_safe,limit=1] run tp @s ~ ~ ~
function rlk:view/sync
# 돌아온 직후 잠깐 무적
scoreboard players set @s dashInvT 20
execute at @e[tag=rlk_safe,limit=1] run particle minecraft:cloud ~ ~0.5 ~ 0.3 0.4 0.3 0.05 14
execute at @e[tag=rlk_safe,limit=1] run particle minecraft:damage_indicator ~ ~1.2 ~ 0.3 0.3 0.3 0.1 6
playsound minecraft:entity.player.hurt master @s ~ ~ ~ 0.9 0.8
playsound minecraft:entity.player.small_fall master @s ~ ~ ~ 0.9 0.7
function rlk:room/msg {t:"추락",c:"#E06A5A"}
