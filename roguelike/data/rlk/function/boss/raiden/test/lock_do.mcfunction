# /function rlk:boss/raiden/test/lock {id:N}: repeat pattern N whenever its phase allows; {id:0} unlocks.
$scoreboard players set #rdReq rd $(id)
execute if score #rdReq rd matches 0 run scoreboard players set #rdLock rd 0
execute if score #rdReq rd matches 0 run scoreboard players set #rdForce rd 0
execute if score #rdReq rd matches 0 run return run tellraw @s [{text:"[보스 테스트] ",color:"light_purple",bold:true},{text:"패턴 고정을 해제했습니다.",color:"gray",bold:false}]
execute store result score #rdOk rd run function rlk:boss/raiden/test/request
execute if score #rdOk rd matches 1 run scoreboard players operation #rdLock rd = #rdReq rd
execute if score #rdOk rd matches 1 run tellraw @s [{text:"[보스 테스트] ",color:"light_purple",bold:true},{text:"패턴 고정: ",color:"gray",bold:false},{score:{name:"#rdReq",objective:"rd"},color:"yellow",bold:false},{text:" (해제: lock {id:0})",color:"gray",bold:false}]
