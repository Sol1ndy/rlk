# 재가 된 만상: 다시 나타나며 벤다 (@s = 플레이어, at 몸). 눈앞의 적 모두(조준이 조금 빗나가도 맞는다)에게 공격력의 150% 불 원소 피해 + 핏값(#arDirDur 틱)
scoreboard players set @s arSk 0
execute if entity @s[tag=rlk_body] run effect clear @s minecraft:invisibility
effect clear @e[tag=rlk_av,limit=1] minecraft:invisibility
item replace entity @e[tag=rlk_av,limit=1] weapon.mainhand from entity @s hotbar.0
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
# 대상: 바로 주변 3칸 + 보는 방향으로 12칸까지(멀수록 넓게: 반경 1.8 + 거리 × 0.25)
tag @e[tag=rlk_mob,distance=..3] add rlk_hit
execute rotated ~ 0 positioned ^ ^ ^2 run tag @e[tag=rlk_mob,distance=..2.3] add rlk_hit
execute rotated ~ 0 positioned ^ ^ ^4 run tag @e[tag=rlk_mob,distance=..2.8] add rlk_hit
execute rotated ~ 0 positioned ^ ^ ^6 run tag @e[tag=rlk_mob,distance=..3.3] add rlk_hit
execute rotated ~ 0 positioned ^ ^ ^8 run tag @e[tag=rlk_mob,distance=..3.8] add rlk_hit
execute rotated ~ 0 positioned ^ ^ ^10 run tag @e[tag=rlk_mob,distance=..4.3] add rlk_hit
execute rotated ~ 0 positioned ^ ^ ^12 run tag @e[tag=rlk_mob,distance=..4.8] add rlk_hit
function rlk:char/dmg_calc {coef:150}
scoreboard players set #elem tmp 1
scoreboard players set #elU tmp 1000
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
execute store result score #ynow tmp run time query gametime
scoreboard players operation #ynow tmp += #arDirDur tmp
scoreboard players operation @e[tag=rlk_hit] arDir = #ynow tmp
execute as @e[tag=rlk_hit] at @s run function rlk:char/arlecchino/mark_fx
execute as @e[tag=rlk_hit,tag=!rlk_armd] at @s run function rlk:char/arlecchino/mk_spawn
tag @e[tag=rlk_hit] remove rlk_hit
execute if score #hitLanded tmp matches 1 run function rlk:char/particles {n:3,el:1}
function rlk:char/after_hit
particle minecraft:flame ~ ~1 ~ 0.4 0.7 0.4 0.08 30
particle minecraft:dust{color:[0.88,0.12,0.20],scale:1.8} ~ ~1 ~ 0.5 0.8 0.5 0 25
particle minecraft:sweep_attack ^ ^1 ^1.5 0.8 0.3 0.8 0 4
playsound minecraft:entity.enderman.teleport master @a ~ ~ ~ 0.4 1.4
playsound minecraft:entity.player.attack.sweep master @a ~ ~ ~ 0.9 0.7
playsound minecraft:entity.blaze.shoot master @a ~ ~ ~ 0.7 0.8
