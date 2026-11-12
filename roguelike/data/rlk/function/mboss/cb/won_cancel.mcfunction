# The fight was cancelled (no kill: /kill, a failed spawn, a reload that lost the body, test/abort): no reward, the gate
# comes back at the zone centre with the same cprep (same texts, same per-map state). Returns nothing (cb/won returns 0).
tellraw @a[tag=player] [{text:"[챕터 보스] ",color:"#E0703A",bold:true},{text:"보스 전투가 취소되었습니다. (보상 없음) 문 오브젝트를 다시 누르면 재도전합니다.",color:"gray",bold:false}]
execute if score #mbTest mb matches 1 if data storage rlk:mboss cur run function rlk:mboss/test/won with storage rlk:mboss cur
function rlk:mboss/forget
function rlk:room/obj/k_cboss
