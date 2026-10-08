# @s = 플레이어, 위치 = 몸. 기본 공격 2타의 추가타: 공격력의 #flurryCoef 퍼센트, 같은 범위(3.5칸), 치명타는 본타격을 따름
# 원소는 본타격과 같음(원소 부여). 6개면 부착 쿨타임을 무시
scoreboard players operation #dmg tmp = @s atk
scoreboard players operation #dmg tmp *= #flurryCoef tmp
scoreboard players operation #dmg tmp /= #100 tmp
execute if score #crit tmp matches 1 run scoreboard players operation #dmg tmp *= @s critDamage
execute if score #crit tmp matches 1 run scoreboard players operation #dmg tmp /= #100 tmp
execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 1
scoreboard players operation #elem tmp = @s infuse
execute unless score #elem tmp matches 0..7 run scoreboard players set #elem tmp 0
scoreboard players set #elU tmp 1000
scoreboard players set #icd tmp 1
execute if score flurry engN matches 6.. run scoreboard players set #icd tmp 0
scoreboard players set #tfm tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #skillDmg tmp 0
scoreboard players set #mobKilled tmp 0
scoreboard players set #killBoss tmp 0
scoreboard players set #killMini tmp 0
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_mob,distance=..3.5] at @s run function rlk:combat/apply_reset
execute anchored eyes run particle minecraft:sweep_attack ^ ^-0.2 ^1.4 0.2 0.1 0.2 0 2
playsound minecraft:entity.player.attack.sweep master @a ~ ~ ~ 0.35 1.9
execute if score #mobKilled tmp matches 1.. run function rlk:combat/on_kill
