# 화살 명중 (@s = 화살): 가장 가까운 적 하나에게 피해. 기본 공격 화살(1·5)은 '기본 공격'으로 친다
scoreboard players set #jend tmp 1
execute if score @s aKind matches 7..8 run return run function rlk:char/ronova/proj_hit
execute if score @s aKind matches 6 run return run function rlk:char/yoimiya/rocket_boom
execute at @s positioned ~-0.75 ~-0.75 ~-0.75 run tag @e[tag=rlk_mob,dx=0.5,dy=0.5,dz=0.5,sort=nearest,limit=1] add rlk_hit
function rlk:combat/clear_atkflags
scoreboard players operation #dmg tmp = @s jdmg
scoreboard players operation #crit tmp = @s jcrit
scoreboard players operation #elem tmp = @s aEl
scoreboard players set #elU tmp 1000
scoreboard players operation #icd tmp = @s aIcd
# 화살은 경직 없음(넉백은 combat/apply 에서)
scoreboard players set #stunHit tmp 0
scoreboard players set #bowHit tmp 1
scoreboard players set #hitLanded tmp 0
scoreboard players set #mobKilled tmp 0
scoreboard players set #killBoss tmp 0
scoreboard players set #killMini tmp 0
scoreboard players operation #aK tmp = @s aKind
execute if score #aK tmp matches 1 run scoreboard players set #basic itv 1
execute if score #aK tmp matches 5 run scoreboard players set #basic itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #bowHit tmp 0
execute if score #basic itv matches 1 if score #hitLanded tmp matches 1 as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:combat/on_hit
# 요이미야: 염초 정화의 춤으로 바뀐 화살이 맞았을 때(원소 입자 · 소매불)
execute if score #aK tmp matches 5 if score #hitLanded tmp matches 1 at @s as @a[tag=player,limit=1] run function rlk:char/yoimiya/blaze_hit
scoreboard players set #basic itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
execute at @s unless score #k238 snd matches 1 run function rlk:snd/f265
execute at @s if score @s aEl matches 1 run particle minecraft:lava ~ ~ ~ 0.15 0.15 0.15 0 4
# 기본 공격 화살: 작은 불꽃 / 콤보 마지막 화살: 폭죽(보기만, 피해는 그대로)
execute at @s if score #aK tmp matches 1 run particle minecraft:firework ~ ~ ~ 0.05 0.05 0.05 0.08 6
execute at @s if score #aK tmp matches 5 run particle minecraft:firework ~ ~ ~ 0.05 0.05 0.05 0.1 10
execute at @s if score #aK tmp matches 5 run particle minecraft:flame ~ ~ ~ 0.1 0.1 0.1 0.05 6
execute at @s if entity @s[tag=rlk_arrfin] run particle minecraft:firework ~ ~ ~ 0.1 0.1 0.1 0.2 35
execute at @s if entity @s[tag=rlk_arrfin] run particle minecraft:dust{color:[1.0,0.55,0.2],scale:1.3} ~ ~ ~ 0.7 0.7 0.7 0 14
execute at @s if entity @s[tag=rlk_arrfin] run particle minecraft:dust{color:[1.0,0.9,0.5],scale:1.0} ~ ~ ~ 0.9 0.9 0.9 0 10
execute at @s if entity @s[tag=rlk_arrfin] unless score #k239 snd matches 1 run function rlk:snd/f266
execute at @s if entity @s[tag=rlk_arrfin] unless score #k240 snd matches 1 run function rlk:snd/f267
kill @s
