# STUB (AP-CORE, ap_contract 1.6): the revival stage; AP-REV replaces this file.
# @s = body (phase 2, every 4 t): line 1 extras (the specials alive, the wave), line 3 (the progress, ⚠).
data modify storage rlk:mboss extra set value []
execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_guard,limit=1] run data modify storage rlk:mboss extra append value {text:"",color:"#F2D45C",extra:[{text:"",font:"rlk:mboss_ap"},{text:"수호"}]}
execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_nest,limit=1] run data modify storage rlk:mboss extra append value {text:"",color:"#C9E07A",extra:[{text:"",font:"rlk:mboss_ap"},{text:"둥지"}]}
execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_nurt,limit=1] run data modify storage rlk:mboss extra append value {text:"",color:"#D4E784",extra:[{text:"",font:"rlk:mboss_ap"},{text:"양육"}]}
execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_pred,limit=1] run data modify storage rlk:mboss extra append value {text:"",color:"#E07A5A",extra:[{text:"",font:"rlk:mboss_ap"},{text:"포식성"}]}
execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_destr,limit=1] run data modify storage rlk:mboss extra append value {text:"",color:"#F0A040",extra:[{text:"",font:"rlk:mboss_ap"},{text:"파괴"}]}
data modify storage rlk:mboss extra append value {text:"  ",color:"#E8E2D0"}
data modify storage rlk:mboss extra append value {score:{name:"#apWave",objective:"mb"},color:"#E8E2D0"}
data modify storage rlk:mboss extra append value {text:"웨이브",color:"#E8E2D0"}
scoreboard players operation #apHtP mb = #apHt mb
scoreboard players operation #apHtP mb /= #c100 mb
data modify storage rlk:mboss sub set value [{text:"소생 진행도 ",color:"#EDCF63"},{score:{name:"#apHtP",objective:"mb"},color:"#EDCF63"},{text:"%",color:"#EDCF63"}]
execute if score #apFail mb matches 1.. run data modify storage rlk:mboss sub append value {text:"  "}
execute if score #apFail mb matches 1.. run data modify storage rlk:mboss sub append value {text:"",color:"#C36E5A",extra:[{text:"",font:"rlk:mboss_ap"}]}
scoreboard players set #apHudQ mb 0
