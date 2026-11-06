# From test/won after a special fight (killed or cancelled): the special wording and replay link (a kill of an entry
# with its own reward word, cur.winWord: test/swon_msg_w, hr FN-a).
execute if score #mbKilled mb matches 1 if data storage rlk:mboss cur.winWord run return run function rlk:mboss/test/swon_msg_w with storage rlk:mboss tlast
execute if score #mbKilled mb matches 1 run return run function rlk:mboss/test/swon_msg with storage rlk:mboss tlast
tellraw @a[tag=player] [{text:"[특수 보스 테스트] ",color:"#E0703A",bold:true},{text:"취소되었습니다(보상 없음). 균열이 다시 열렸습니다. ",color:"gray",bold:false},{text:"[로비로]",color:"yellow",bold:false,click_event:{action:"suggest_command",command:'/function rlk:mboss/test/stop'}}]
