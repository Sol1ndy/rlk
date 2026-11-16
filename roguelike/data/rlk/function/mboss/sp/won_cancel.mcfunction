# The fight was cancelled (no kill: /kill, a failed spawn, a reload that lost the body, test/abort, the arena never got
# ready): no reward, the rift reopens (room/rift/reopen) and can be entered again.
tellraw @a[tag=player] [{text:"[특수 보스] ",color:"#E0703A",bold:true},{text:"특수 보스 전투가 취소되었습니다. (보상 없음) 균열에 다시 들어가면 재도전합니다.",color:"gray",bold:false}]
execute if score #mbTest mb matches 1 if data storage rlk:mboss cur run function rlk:mboss/test/won with storage rlk:mboss cur
function rlk:mboss/forget
scoreboard players operation #spZ mb = @s zid
execute as @e[type=minecraft:marker,tag=rlk_rift] if score @s zid = #spZ mb at @s run function rlk:room/rift/reopen
