# 로노바 투사체 명중 (@s = 투사체). 잔향 = 범위 폭발, 구체 = 가장 가까운 적 하나에게 공허 원소 피해(일반 공격)
execute if score @s aKind matches 8 run return run function rlk:char/ronova/echo_boom
execute at @s positioned ~-0.75 ~-0.75 ~-0.75 run tag @e[tag=rlk_mob,dx=0.5,dy=0.5,dz=0.5,sort=nearest,limit=1] add rlk_hit
function rlk:combat/clear_atkflags
scoreboard players operation #dmg tmp = @s jdmg
scoreboard players operation #crit tmp = @s jcrit
scoreboard players set #elem tmp 8
scoreboard players set #elU tmp 1000
scoreboard players operation #icd tmp = @s aIcd
scoreboard players set #stunHit tmp 0
scoreboard players set #bowHit tmp 1
scoreboard players set #hitLanded tmp 0
scoreboard players set #mobKilled tmp 0
scoreboard players set #killBoss tmp 0
scoreboard players set #killMini tmp 0
scoreboard players set #basic itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
scoreboard players set #bowHit tmp 0
execute if score #hitLanded tmp matches 1 as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:combat/on_hit
scoreboard players set #basic itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
execute at @s run particle minecraft:dust{color:[0.88,0.12,0.22],scale:1.3} ~ ~ ~ 0.15 0.15 0.15 0 8
execute at @s run particle minecraft:dust{color:[0.10,0.02,0.05],scale:1.0} ~ ~ ~ 0.1 0.1 0.1 0 4
execute at @s if entity @s[scores={aIcd=0}] run particle minecraft:reverse_portal ~ ~ ~ 0.1 0.1 0.1 0.3 12
execute at @s run playsound minecraft:block.amethyst_cluster.break master @a ~ ~ ~ 0.4 1.3
execute at @s if entity @s[scores={aIcd=0}] run playsound minecraft:entity.wither.shoot master @a ~ ~ ~ 0.15 1.9
execute at @s if entity @s[scores={aIcd=0}] run playsound minecraft:block.respawn_anchor.deplete master @a ~ ~ ~ 0.3 1.6
kill @s
