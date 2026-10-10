# 수호 4개 (@s = 플레이어): 보호막이 없고 재생 대기가 끝났으면 다시 생김
execute if score @s gShield matches 1.. run scoreboard players operation 수호보호막 stacks = @s gShield
execute if score @s gShield matches 1.. run return run scoreboard players display name 수호보호막 stacks {text:"수호 보호막",color:"#6FB1FF"}
scoreboard players reset 수호보호막 stacks
execute if score @s gCd matches 1.. run scoreboard players remove @s gCd 1
execute if score @s gCd matches 1.. run return 0
scoreboard players operation @s gShield = #guardAmt tmp
execute at @e[tag=rlk_body,limit=1] unless score #k213 snd matches 1 run function rlk:snd/f236
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.44f,0.69f,1.0f],scale:1.2f} ~ ~1 ~ 0.5 0.8 0.5 0 30
