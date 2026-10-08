# @s = 골드 조각. 골드 획득(각인 보물 2개면 증가)
execute if entity @s[tag=rlk_sap] run return run function rlk:combat/sap_absorb
scoreboard players operation #gain tmp = @s gval
execute if score treasure engN matches 2.. run function rlk:engravings/treasure/gain
execute if score #gain tmp matches ..0 run scoreboard players set #gain tmp 1
scoreboard players operation @a[tag=player,limit=1] gold += #gain tmp
execute as @a[tag=player,limit=1] at @s run playsound minecraft:entity.experience_orb.pickup master @s ~ ~ ~ 0.35 1.7
kill @s
