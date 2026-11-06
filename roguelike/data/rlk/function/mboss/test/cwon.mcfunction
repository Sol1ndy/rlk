# From test/won after a chapter fight (killed or cancelled): the forced routing and the auto gate press end with the
# fight (cm.md 4.1; a cancelled gate needs neither: cb/gate and cb/start never read #cbForce), so the rest of the
# session (k_chapter -> the next chapter's boss map) routes as in a run. The chapter wording and replay link.
scoreboard players set #cbForce mb 0
scoreboard players set #cbAuto mb 0
execute if score #mbKilled mb matches 1 run return run function rlk:mboss/test/cwon_msg with storage rlk:mboss tlast
tellraw @a[tag=player] [{text:"[챕터 보스 테스트] ",color:"#E0703A",bold:true},{text:"취소되었습니다(보상 없음). 문이 다시 나타났습니다. ",color:"gray",bold:false},{text:"[로비로]",color:"yellow",bold:false,click_event:{action:"suggest_command",command:'/function rlk:mboss/test/stop'}}]
