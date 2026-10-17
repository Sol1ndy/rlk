# From player/hook_respawn during a test: never fails/resets the character.
function rlk:mboss/test/end
title @s times 10 40 15
title @s subtitle {text:"로비로 돌아왔습니다",color:"gray"}
title @s title {text:"중간보스 테스트 실패",color:"#E06A5A",bold:true}
scoreboard players set @s vBig 65
scoreboard players set @s ttlT 65
tellraw @s [{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},{text:"쓰러졌습니다. ",color:"gray",bold:false},{text:"[다시 하기]",color:"yellow",bold:false,click_event:{action:"suggest_command",command:'/function rlk:mboss/test/start {id:"proto"}'}}]
