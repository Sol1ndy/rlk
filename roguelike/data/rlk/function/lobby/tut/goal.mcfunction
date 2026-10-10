# 목표 줄 다시 쓰기 (#tutC / #tutNeed)
scoreboard players operation #tutCp lob = #tutC lob
execute store result storage rlk:lobby gc int 1 run scoreboard players get #tutC lob
execute store result storage rlk:lobby gn int 1 run scoreboard players get #tutNeed lob
execute if score #tutNeed lob matches 0 if score #tutS lob matches 11 run return run data modify entity @e[tag=rlk_tutg,limit=1] text set value {text:"「캐릭터 튜토리얼」 또는 「로비로」",color:"#FFE08A"}
execute if score #tutNeed lob matches 0 if score #tutS lob matches 26 run return run data modify entity @e[tag=rlk_tutg,limit=1] text set value {text:"「캐릭터 바꾸기」로 다른 캐릭터도 해 보세요",color:"#FFE08A"}
execute if score #tutNeed lob matches 0 run return run data modify entity @e[tag=rlk_tutg,limit=1] text set value {text:"다 읽었으면 「다음 단계 ▶」를 누르세요",color:"#FFE08A"}
execute if score #tutW lob matches 1.. run return run data modify entity @e[tag=rlk_tutg,limit=1] text set value {text:"✔ 완료! 잠시 뒤 다음 단계로",color:"#7BE07B",bold:true}
function rlk:lobby/tut/goal_m with storage rlk:lobby
