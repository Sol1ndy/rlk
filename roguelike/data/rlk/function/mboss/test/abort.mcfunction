# Removes the body without a kill: the zone clears and mboss/won cancels (no reward, gate back).
execute unless entity @e[tag=rlk_mb_body,limit=1] run return run tellraw @s [{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},{text:"진행 중인 중간보스가 없습니다.",color:"gray",bold:false}]
kill @e[tag=rlk_mb_body]
execute unless score #combat room matches 1.. run function rlk:mboss/cleanup
tellraw @s [{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},{text:"중간보스를 보상 없이 없앴습니다(취소 경로).",color:"gray",bold:false}]
