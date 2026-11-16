execute unless score #mbTest mb matches 1 run return run tellraw @s [{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},{text:"진행 중인 중간보스 테스트가 없습니다.",color:"gray",bold:false}]
function rlk:mboss/test/end
tellraw @a[tag=player] [{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},{text:"중간보스 테스트를 끝내고 로비로 돌아왔습니다.",color:"gray",bold:false}]
