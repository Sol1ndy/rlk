$scoreboard players set #mbReq mb $(lv)
execute unless score #mbReq mb matches 1..999 run return run tellraw @s [{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},{text:"레벨은 1 이상이어야 합니다.",color:"gray",bold:false}]
execute unless entity @e[tag=rlk_mb_body,limit=1] run return run tellraw @s [{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},{text:"진행 중인 중간보스가 없습니다.",color:"gray",bold:false}]
execute as @e[tag=rlk_mb_body,limit=1] run scoreboard players operation @s mlv = #mbReq mb
execute as @e[tag=rlk_mb_body,limit=1] run function rlk:mob/level_apply
scoreboard players operation #mbLv mb = #mbReq mb
# chapter mode (AZ-CM): the new full pool is #mbTot; the current split (#mbPoolPct < 100) is applied again
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run scoreboard players operation #mbTot mb = @s mhpM
execute if score #mbPoolPct mb matches 1..99 store result storage rlk:mboss a.pct int 1 run scoreboard players get #mbPoolPct mb
execute if score #mbPoolPct mb matches 1..99 run function rlk:mboss/repool with storage rlk:mboss a
tellraw @s [{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},{text:"중간보스 레벨을 바꾸고 체력을 다시 채웠습니다.",color:"gray",bold:false}]
