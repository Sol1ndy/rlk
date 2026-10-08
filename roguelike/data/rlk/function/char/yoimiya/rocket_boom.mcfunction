# 유금 운간초 폭발 (@s = 불화살): 반경 5칸 불 원소 피해 + 맞은 적 모두에게 유금화광(#yoiAurDur 틱)
scoreboard players set #jend tmp 1
execute at @s run tag @e[tag=rlk_mob,distance=..5] add rlk_hit
function rlk:combat/clear_atkflags
scoreboard players operation #dmg tmp = @s jdmg
scoreboard players operation #crit tmp = @s jcrit
scoreboard players set #skillDmg tmp 1
scoreboard players set #stunHit tmp 1
scoreboard players set #elem tmp 1
scoreboard players set #elU tmp 1000
scoreboard players set #hitLanded tmp 0
scoreboard players set #mobKilled tmp 0
scoreboard players set #killBoss tmp 0
scoreboard players set #killMini tmp 0
scoreboard players operation #dmgBase tmp = #dmg tmp
# 원소폭발 자신은 유금화광을 터뜨리지 않는다
scoreboard players set #yoiBoom tmp 1
execute as @e[tag=rlk_hit] at @s run function rlk:combat/apply_reset
scoreboard players set #yoiBoom tmp 0
execute store result score #ynow tmp run time query gametime
scoreboard players operation #ynow tmp += #yoiAurDur tmp
scoreboard players operation @e[tag=rlk_hit] aurEnd = #ynow tmp
tag @e[tag=rlk_hit] remove rlk_hit
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
execute at @s run particle minecraft:explosion ~ ~ ~ 1.5 1.0 1.5 0 6
execute at @s run particle minecraft:firework ~ ~ ~ 0.5 0.5 0.5 0.35 80
execute at @s run particle minecraft:flame ~ ~ ~ 1.5 1.0 1.5 0.12 80
execute at @s run particle minecraft:dust{color:[1.0f,0.75f,0.2f],scale:2.2f} ~ ~ ~ 2.2 1.2 2.2 0 40
execute at @s run playsound minecraft:entity.firework_rocket.large_blast master @a ~ ~ ~ 1.2 0.9
execute at @s run playsound minecraft:entity.firework_rocket.twinkle master @a ~ ~ ~ 1.0 1.0
execute at @s run playsound minecraft:entity.generic.explode master @a ~ ~ ~ 0.5 1.4
kill @s
