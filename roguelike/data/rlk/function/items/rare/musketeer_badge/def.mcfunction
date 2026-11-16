# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.musketeer_badge set value {item:"minecraft:firework_star",name:"특순대 휘장",type:"accessory",rarity:"rare",stats:{atkPct:6},abilities:[{text:"",extra:[{text:"과부하 반응을 일으키면 한동안 공격력이 증가한다."}]},{text:""},{text:"",extra:[{text:"공격력 증가: "},{tk:{c:"#muskAtk",x:1,d:1,p:0,u:"%"},color:"#FFE08A"}]},{text:"",extra:[{text:"지속 시간: "},{tk:{c:"#muskDur",x:1,d:20,p:1,u:"초"},color:"#FFE08A"}]}],desc:["화약 냄새가 밴 휘장."],engravings:["thunder","spirit"]}
data modify storage rlk:items ids append value "musketeer_badge"
