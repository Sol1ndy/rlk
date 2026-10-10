# From player/hook_respawn (@s = respawned player): a lost test never fails/resets the run.
function rlk:boss/raiden/test/end
title @s times 10 40 15
title @s subtitle {text:"로비로 돌아왔습니다",color:"gray"}
title @s title {text:"보스 테스트 실패",color:"#E06A5A",bold:true}
tellraw @s [{text:"[보스 테스트] ",color:"light_purple",bold:true},{text:"쓰러졌습니다. 다시 도전: ",color:"gray",bold:false},{text:"/function rlk:boss/raiden/test/start",color:"yellow",bold:false,click_event:{action:"suggest_command",command:"/function rlk:boss/raiden/test/start"}}]
