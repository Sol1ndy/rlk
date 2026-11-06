# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.captain_bracer set value {item:"minecraft:nether_brick",name:"선장의 팔보호대",type:"accessory",rarity:"common",stats:{defPct:10},abilities:[{text:"",extra:[{text:"받는 피해가 감소한다."}]},{text:""},{text:"",extra:[{text:"받는 피해 감소: "},{tk:{c:"#bracerRes",x:1,d:10,p:1,u:"%"},color:"#FFE08A"}]}],desc:["파도는 정면으로 받아내는 것이다."],engravings:["vajra","guard"]}
data modify storage rlk:items ids append value "captain_bracer"
