# From room/obj/click (oact 16; @s = the gate object, at it; clicks during combat are refused there). The guards of
# mboss/gate, "준비 중" while an arena job runs (#mbArBuild >= 1: the object stays), then the boss's own gate (cb/g/<id>).
execute store result score #mbDiff mb run difficulty
execute if score #mbDiff mb matches 0 run return run tellraw @a[tag=player] [{text:"[챕터 보스] ",color:"#E0703A",bold:true},{text:"난이도가 '평화로움'이면 보스가 나타나지 않습니다. /difficulty easy 이상으로 바꾼 뒤 다시 누르세요.",color:"gray",bold:false}]
tag @e[tag=rlk_cbz] remove rlk_cbz
execute as @e[tag=rlk_zone,scores={zkind=9,zst=3}] if data entity @s data.cboss run tag @s add rlk_cbz
execute unless entity @e[tag=rlk_cbz,limit=1] run return 0
execute if entity @e[tag=rlk_mb_body,limit=1] run return run tag @e[tag=rlk_cbz] remove rlk_cbz
execute if score #mbArBuild mb matches 1.. run tag @e[tag=rlk_cbz] remove rlk_cbz
execute if score #mbArBuild mb matches 1.. run return run tellraw @a[tag=player] [{text:"[챕터 보스] ",color:"#E0703A",bold:true},{text:"경기장을 준비하는 중입니다. 잠시 뒤 다시 누르세요.",color:"gray",bold:false}]
data modify storage rlk:mboss cbg set value ""
data modify storage rlk:mboss cbg set from entity @e[tag=rlk_cbz,limit=1] data.boss_id
execute if data storage rlk:mboss {cbg:"cproto"} run return run function rlk:mboss/cb/g/cproto
execute if data storage rlk:mboss {cbg:"apep"} run return run function rlk:mboss/cb/g/apep
tag @e[tag=rlk_cbz] remove rlk_cbz
