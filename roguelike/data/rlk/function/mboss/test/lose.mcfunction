# The objective-loss path of the chapter mode (mboss/cb/lose): the normal death (test/defeat in a test).
execute unless entity @e[tag=rlk_mb_body,limit=1] run return run tellraw @s [{text:"[챕터 보스 테스트] ",color:"#E0703A",bold:true},{text:"진행 중인 보스가 없습니다.",color:"gray",bold:false}]
function rlk:mboss/cb/lose
