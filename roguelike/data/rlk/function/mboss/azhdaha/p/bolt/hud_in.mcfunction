data modify storage rlk:mboss az.subx set value [{text:"  안전 지대 안",color:"#2FCF5E",bold:true}]
execute unless score #aq42In mb matches 1 at @e[tag=rlk_body,limit=1] run function rlk:mboss/azhdaha/fx/snd/safe_chime
scoreboard players set #aq42In mb 1
