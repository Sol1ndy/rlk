# from rlk:uninstall: groggy mobs get their AI back, the rows go, the scores and the tables go
execute as @e[tag=rlk_bal_grog] run function rlk:bal/grog/clear
tag @e[tag=rlk_bal_pend] remove rlk_bal_pend
kill @e[tag=rlk_hb_bal]
scoreboard objectives remove bal
scoreboard objectives remove balMax
scoreboard objectives remove balT
scoreboard objectives remove grgT
scoreboard objectives remove balC
scoreboard objectives remove balF
scoreboard objectives remove balQ
scoreboard objectives remove balX
data remove storage rlk:bal h4
data remove storage rlk:bal h7
data remove storage rlk:bal b12
data remove storage rlk:bal brow
data remove storage rlk:bal a
