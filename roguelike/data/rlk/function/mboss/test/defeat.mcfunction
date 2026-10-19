# From player/hook_respawn during a test: never fails/resets the character. The replay link restarts the boss and
# the chapter of this test (rlk:mboss tlast {id, ch}, saved by test/start_ch; cur is forgotten by test/end).
execute unless data storage rlk:mboss tlast.id run data modify storage rlk:mboss tlast set value {id:"proto",ch:1}
execute if data storage rlk:mboss cur.id run data modify storage rlk:mboss tlast.id set from storage rlk:mboss cur.id
execute unless data storage rlk:mboss tlast.ch run data modify storage rlk:mboss tlast.ch set value 1
function rlk:mboss/test/end
title @s times 10 40 15
title @s subtitle {text:"로비로 돌아왔습니다",color:"gray"}
execute unless data storage rlk:mboss tlast{cb:1b} run title @s title {text:"중간보스 테스트 실패",color:"#E06A5A",bold:true}
execute if data storage rlk:mboss tlast{cb:1b} run title @s title {text:"챕터 보스 테스트 실패",color:"#E06A5A",bold:true}
scoreboard players set @s vBig 65
scoreboard players set @s ttlT 65
execute if data storage rlk:mboss tlast{cb:1b} run return run function rlk:mboss/test/cdefeat_msg with storage rlk:mboss tlast
function rlk:mboss/test/defeat_msg with storage rlk:mboss tlast
