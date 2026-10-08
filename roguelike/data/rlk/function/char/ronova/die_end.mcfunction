# 되살아남 (@s = 플레이어)
scoreboard players set @s rnDie 0
scoreboard players operation @s curHealth = @s maxHealth
scoreboard players operation @s curHealth *= #rnRevPct tmp
scoreboard players operation @s curHealth /= #100 tmp
execute if score @s curHealth matches ..0 run scoreboard players set @s curHealth 1
attribute @s minecraft:movement_speed modifier remove rlk:ronova_die
attribute @s minecraft:jump_strength modifier remove rlk:ronova_die
effect clear @s minecraft:darkness
execute as @e[tag=rlk_av,limit=1] run data modify entity @s pose set value "standing"
# 명계의 반동
execute at @e[tag=rlk_body,limit=1] run function rlk:char/ronova/rev_wave
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.88,0.12,0.22],scale:2.0} ~ ~1 ~ 0.5 1 0.5 0 60
execute at @e[tag=rlk_body,limit=1] run particle minecraft:reverse_portal ~ ~1 ~ 0.5 1 0.5 0.5 60
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:item.totem.use master @a ~ ~ ~ 0.6 0.6
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:entity.elder_guardian.curse master @a ~ ~ ~ 0.5 0.8
