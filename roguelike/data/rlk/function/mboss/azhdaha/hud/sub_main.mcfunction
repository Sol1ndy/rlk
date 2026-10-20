execute if score #azLastHit mb matches 1 run return run data modify storage rlk:mboss sub append value {text:"마지막 일격!",color:"#FFD27A",bold:true}
execute if score #azCue mb matches 1.. run return run data modify storage rlk:mboss sub append value {text:"점프!",color:"#FFFFFF",bold:true}
execute if score #azBur mb matches 1 if score #azTail mb matches 3 run return run data modify storage rlk:mboss sub append value {text:"꼬리만 공격할 수 있습니다",color:"#C58BFF",bold:true}
execute if score #azBur mb matches 1 if score #azTail mb matches 4 run return run data modify storage rlk:mboss sub append value {text:"꼬리만 공격할 수 있습니다",color:"#9FE8F5",bold:true}
execute if score #azTr mb matches 1.. if score #azTrN mb matches 1 if score #azLeg mb matches 1 run return run data modify storage rlk:mboss sub append value {text:"야타용왕이 곧 불 원소의 힘을 흡수합니다…",color:"#FF8A3D",bold:true}
execute if score #azTr mb matches 1.. if score #azTrN mb matches 1 if score #azLeg mb matches 2 run return run data modify storage rlk:mboss sub append value {text:"야타용왕이 곧 물 원소의 힘을 흡수합니다…",color:"#4FB8FF",bold:true}
execute if score #azTr mb matches 1.. if score #azTrN mb matches 2 if score #azTail mb matches 3 run return run data modify storage rlk:mboss sub append value {text:"야타용왕이 곧 번개 원소의 힘을 흡수합니다…",color:"#C58BFF",bold:true}
execute if score #azTr mb matches 1.. if score #azTrN mb matches 2 if score #azTail mb matches 4 run return run data modify storage rlk:mboss sub append value {text:"야타용왕이 곧 얼음 원소의 힘을 흡수합니다…",color:"#9FE8F5",bold:true}
execute if score #azHint mb matches 1 if score #azHintT mb > #azClk mb run return run data modify storage rlk:mboss sub append value {text:"꼬리를 높이 들면: 머리 정면으로 들어가거나 꼬리 반대편으로 넘어가세요",color:"#FFE3A8",bold:false}
execute if score #azHint mb matches 2 if score #azHintT mb > #azClk mb run return run data modify storage rlk:mboss sub append value {text:"옆구리 금지 — 머리 정면 · 꼬리 끝",color:"#FFE3A8",bold:false}
execute if score #azHint mb matches 3 if score #azHintT mb > #azClk mb run return run data modify storage rlk:mboss sub append value {text:"응결 결정 — 주우면 보호막",color:"#FFE3A8",bold:false}
execute if score #azPat mb matches 1 run return run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"갈라지는 봉인의 땅",color:"#F2E2B0",bold:false}]
execute if score #azPat mb matches 2 run return run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"바위 분쇄 충돌",color:"#F2E2B0",bold:false}]
execute if score #azPat mb matches 3 run return run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"바위 용왕의 돌진",color:"#F2E2B0",bold:false}]
execute if score #azPat mb matches 4 run return run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"천동만상",color:"#F2E2B0",bold:false}]
execute if score #azPat mb matches 5 run return run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"산명곡응",color:"#F2E2B0",bold:false}]
execute if score #azPat mb matches 10 run return run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"산명곡응 – 연속 발구르기",color:"#F2E2B0",bold:false}]
execute if score #azPat mb matches 6 run return run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"성동격서",color:"#F2E2B0",bold:false}]
execute if score #azPat mb matches 7 run return run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"교활한 통수",color:"#F2E2B0",bold:false}]
execute if score #azPat mb matches 8 run return run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"꼬리찍기",color:"#F2E2B0",bold:false}]
execute if score #azPat mb matches 9 run return run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"잠복 돌진",color:"#F2E2B0",bold:false}]
execute if score #azPat mb matches 43 run return run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"쏟아지는 천화",color:"#F2E2B0",bold:false}]
execute if score #azPat mb matches 44 run return run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"번개의 가루",color:"#F2E2B0",bold:false}]
execute if score #azPat mb matches 45 run return run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"천동만상 – 얼음 가시",color:"#F2E2B0",bold:false}]
execute if score #azPat mb matches 46 run return run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"천동만상 – 번개 가시",color:"#F2E2B0",bold:false}]
execute if score #azPat mb matches 30 run return run data modify storage rlk:mboss sub set value [{text:"패턴  ",color:"#A8A8A8"},{text:"원소 특수 공격",color:"#F2E2B0",bold:false}]
