# /function rlk:boss/raiden/test/pattern {id:N}: N = 1~6 (normal) or 11~18 (armored), once.
$scoreboard players set #rdReq rd $(id)
execute store result score #rdOk rd run function rlk:boss/raiden/test/request
execute if score #rdOk rd matches 1 run scoreboard players operation #rdForce rd = #rdReq rd
execute if score #rdOk rd matches 1 run tellraw @s [{text:"[보스 테스트] ",color:"light_purple",bold:true},{text:"다음 패턴: ",color:"gray",bold:false},{score:{name:"#rdReq",objective:"rd"},color:"yellow",bold:false}]
