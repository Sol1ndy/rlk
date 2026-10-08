function rlk:char/dmg_calc {coef:30}
scoreboard players set #sub itv 1
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 3
scoreboard players set #elU tmp 1000
tag @e[tag=rlk_mob,distance=..12,sort=nearest,limit=1] add rlk_abt
scoreboard players set #aqE eng 3
scoreboard players set #bi eng 0
execute at @e[tag=rlk_raven,limit=1] facing entity @e[tag=rlk_abt,limit=1] eyes run function rlk:items/fx/shot
playsound minecraft:entity.bee.sting master @a ~ ~ ~ 0.4 1.6
execute as @e[tag=rlk_abt,limit=1] at @s run function rlk:combat/apply
tag @e[tag=rlk_abt] remove rlk_abt
function rlk:char/after_hit
scoreboard players set #sub itv 0
