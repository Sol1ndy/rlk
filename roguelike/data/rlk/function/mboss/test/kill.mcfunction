# Lethal true hit through combat/apply: pays like a real kill (reward path).
execute unless entity @e[tag=rlk_mb_body,limit=1] run return run tellraw @s [{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},{text:"진행 중인 중간보스가 없습니다.",color:"gray",bold:false}]
execute if score #mbSt mb matches 0 run function rlk:mboss/intro_end
execute as @e[tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/test/kill_do
