# 참격 한 번 (@s = 플레이어, 위치·방향 = 발동한 자리, macro: coef). 전방(3.5칸 앞을 중심으로 반경 4.5칸 + 발동 자리 반경 2칸)에 얼음 원소 피해
# 피해 = 공격력 × coef% + 공격력 × 초과한 뱀의 계략(pt) × #skPtBonus/100 %
$function rlk:char/dmg_calc {coef:$(coef)}
scoreboard players operation #pb tmp = @s atk
scoreboard players operation #pb tmp *= @s skPts
scoreboard players operation #pb tmp *= #skPtBonus tmp
scoreboard players operation #pb tmp /= #10000 tmp
execute if score #crit tmp matches 1 run scoreboard players operation #pb tmp *= @s critDamage
execute if score #crit tmp matches 1 run scoreboard players operation #pb tmp /= #100 tmp
scoreboard players operation #dmg tmp += #pb tmp
function rlk:items/hook/burst_dmg
scoreboard players set #elem tmp 4
scoreboard players set #elU tmp 1000
tag @e[tag=rlk_mob,distance=..2] add rlk_hit
execute positioned ^ ^ ^3.5 run tag @e[tag=rlk_mob,distance=..4.5] add rlk_hit
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
execute at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
execute positioned ^ ^1 ^3 run particle minecraft:sweep_attack ~ ~ ~ 1.8 0.8 1.8 0 6
execute positioned ^ ^1 ^3 run particle minecraft:snowflake ~ ~ ~ 1.8 0.8 1.8 0.05 20
execute positioned ^ ^1 ^3 run particle minecraft:dust{color:[0.75f,0.6f,1.0f],scale:1.4f} ~ ~ ~ 2.0 0.9 2.0 0 14
playsound minecraft:entity.player.attack.sweep master @a ~ ~ ~ 0.8 1.9
playsound minecraft:block.glass.break master @a ~ ~ ~ 0.35 1.8
