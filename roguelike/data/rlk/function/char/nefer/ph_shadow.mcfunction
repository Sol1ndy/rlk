# 환영극 · 그림자 (@s = 플레이어): 노리는 자리를 대각선으로 가로질러(도착 각도 a) 반경 2.5칸에 달 개화 피해. 기본 피해 = 원소 마스터리 × e% × (100 + 장막 × 8)%
$function rlk:char/nefer/shadow_move {a:$(a)}
execute as @e[tag=rlk_nfsh] run swing @s mainhand
execute store result score #lnB tmp run scoreboard players get @s elemMastery
execute if score #lnB tmp matches ..0 run scoreboard players set #lnB tmp 1
$scoreboard players set #t1 tmp $(e)
scoreboard players operation #lnB tmp *= #t1 tmp
scoreboard players operation #lnB tmp /= #100 tmp
scoreboard players operation #t1 tmp = @s nfVeil
scoreboard players operation #t1 tmp *= #c8 tmp
scoreboard players add #t1 tmp 100
scoreboard players operation #lnB tmp *= #t1 tmp
scoreboard players operation #lnB tmp /= #100 tmp
scoreboard players set #lnEl tmp 7
scoreboard players set #lnT tmp 2
scoreboard players set #hitLanded tmp 0
scoreboard players set #mobKilled tmp 0
execute at @e[tag=rlk_nfsp,limit=1] as @e[tag=rlk_mob,distance=..2.5] at @s run function rlk:char/nefer/ph_shadow_hit
execute at @e[tag=rlk_nfsp,limit=1] run function rlk:char/nefer/shadow_fx
function rlk:char/after_hit
