# Scheduled every 5 t after test/special_ch (at most 600 t): enters the open rift once no arena job runs (#spAuto 1).
execute unless score #spAuto mb matches 1 run return 0
execute unless score #mbTest mb matches 1 run return run scoreboard players set #spAuto mb 0
scoreboard players add #spWaitT mb 5
execute if score #mbArBuild mb matches 0 if score #combat room matches 0 as @e[type=minecraft:marker,tag=rlk_rift,scores={riftS=2},limit=1] at @s run return run function rlk:mboss/test/spress
execute if score #spWaitT mb matches 600.. run return run function rlk:mboss/test/stimeout
schedule function rlk:mboss/test/swait 5t replace
