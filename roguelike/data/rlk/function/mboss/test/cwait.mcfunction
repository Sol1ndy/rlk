# Scheduled every 5 t after test/chapter_ch (at most 300 t): presses the gate once no arena job runs (#cbAuto 1).
execute unless score #cbAuto mb matches 1 run return 0
execute unless score #mbTest mb matches 1 run return run scoreboard players set #cbAuto mb 0
scoreboard players add #cbWaitT mb 5
execute if score #mbArBuild mb matches 0 if entity @e[tag=rlk_obj,scores={oact=16},limit=1] run return run function rlk:mboss/test/cpress
execute if score #cbWaitT mb matches 300.. run return run function rlk:mboss/test/ctimeout
schedule function rlk:mboss/test/cwait 5t replace
