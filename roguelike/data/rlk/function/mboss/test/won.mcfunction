# From mboss/won during a test (with storage rlk:mboss cur): the replay link comes from rlk:mboss tlast {id, ch}
# (test/start_ch), with this fight's id.
$data modify storage rlk:mboss tlast.id set value "$(id)"
execute unless data storage rlk:mboss tlast.ch run data modify storage rlk:mboss tlast.ch set value 1
# the wording follows this fight (cur.kind; cur is always there), not the session: a chapter test can go on to a
# mid-boss of the next chapter and back (tlast.cb is kept for test/defeat)
execute if data storage rlk:mboss cur{kind:"chapter"} run data modify storage rlk:mboss tlast.cb set value 1b
execute unless data storage rlk:mboss cur{kind:"chapter"} run data remove storage rlk:mboss tlast.cb
execute if data storage rlk:mboss cur{kind:"chapter"} run return run function rlk:mboss/test/cwon
# special bosses (Tachy S1): their wording and replay link (test/swon)
execute if data storage rlk:mboss cur{kind:"special"} run data modify storage rlk:mboss tlast.sp set value 1b
execute unless data storage rlk:mboss cur{kind:"special"} run data remove storage rlk:mboss tlast.sp
execute if data storage rlk:mboss cur{kind:"special"} run return run function rlk:mboss/test/swon
execute if score #mbKilled mb matches 1 run function rlk:mboss/test/won_msg with storage rlk:mboss tlast
execute unless score #mbKilled mb matches 1 run tellraw @a[tag=player] [{text:"[중간보스 테스트] ",color:"#E0703A",bold:true},{text:"취소되었습니다(보상 없음). ",color:"gray",bold:false},{text:"[로비로]",color:"yellow",bold:false,click_event:{action:"suggest_command",command:'/function rlk:mboss/test/stop'}}]
