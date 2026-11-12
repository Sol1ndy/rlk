# #mbLock mb = N: the module repeats pattern N (0 unlocks). Modules read it in their pattern choice.
$scoreboard players set #mbLock mb $(id)
$tellraw @s [{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},{text:"패턴 고정: $(id) (0 = 해제)",color:"gray",bold:false}]
