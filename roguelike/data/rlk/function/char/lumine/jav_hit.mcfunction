# 투창 명중 (@s = 투창): 맞은 적과 주변 2칸에 피해
scoreboard players set #jend tmp 1
execute at @s positioned ~-1 ~-1 ~-1 run tag @e[tag=rlk_mob,dx=1,dy=1,dz=1] add rlk_hit
execute at @s positioned ~ ~-1 ~ run tag @e[tag=rlk_mob,distance=..2] add rlk_hit
function rlk:combat/clear_atkflags
scoreboard players operation #dmg tmp = @s jdmg
scoreboard players operation #crit tmp = @s jcrit
scoreboard players set #skillDmg tmp 1
scoreboard players set #stunHit tmp 1
scoreboard players set #elem tmp 4
scoreboard players set #elU tmp 1000
scoreboard players set #icd tmp 1
scoreboard players set #hitLanded tmp 0
scoreboard players set #mobKilled tmp 0
scoreboard players set #killBoss tmp 0
scoreboard players set #killMini tmp 0
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hit] remove rlk_hit
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
function rlk:char/lumine/jav_break
