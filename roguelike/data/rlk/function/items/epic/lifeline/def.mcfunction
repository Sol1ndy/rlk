# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.lifeline set value {item:"minecraft:lead",name:"생명줄",type:"accessory",rarity:"epic",stats:{hpPct:15},abilities:[{text:"",extra:[{text:"대쉬로 지나친 적에게 실이 감긴다."}]},{text:"",extra:[{text:"대쉬가 끝나면 실이 감긴 모든 적에게 "},{text:"물 원소 피해",color:"#4FB8FF"},{text:"를 준다."}]},{text:""},{text:"",extra:[{text:"피해: "},{text:"최대 체력의 8%",color:"#FFE08A"}]}],desc:["끊어질 듯 이어지는 것이 인연이다."],engravings:["tide","dash"]}
data modify storage rlk:items ids append value "lifeline"
