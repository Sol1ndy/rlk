# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.holy_shield set value {item:"minecraft:turtle_scute",name:"성스러운 방패",type:"accessory",rarity:"rare",stats:{hpPct:10},abilities:[{text:"",extra:[{text:"원소폭발을 쓰면 한동안 기본 공격 피해가 증가한다."}]},{text:""},{text:"",extra:[{text:"피해 증가: "},{tk:{c:"#candDmg",x:1,d:1,p:0,u:"%"},color:"#FFE08A"}]},{text:"",extra:[{text:"지속 시간: "},{tk:{c:"#candDur",x:1,d:20,p:1,u:"초"},color:"#FFE08A"}]}],desc:["사막의 후예는 물러서지 않는다."],engravings:["tide","chain"]}
data modify storage rlk:items ids append value "holy_shield"
