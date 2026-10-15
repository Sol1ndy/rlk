# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.prayer_beads set value {item:"minecraft:heart_pottery_sherd",name:"기도 묵주",type:"accessory",rarity:"common",stats:{hpPct:8},abilities:[{text:"",extra:[{text:"받는 치유량이 증가한다."}]},{text:""},{text:"",extra:[{text:"치유량 증가: "},{tk:{c:"#beadsHeal",x:1,d:1,p:0,u:"%"},color:"#FFE08A"}]}],desc:["노래를 부르면 조금 덜 아프다고 한다."],engravings:["tide","unyielding"]}
data modify storage rlk:items ids append value "prayer_beads"
