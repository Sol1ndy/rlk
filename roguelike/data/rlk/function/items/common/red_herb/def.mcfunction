# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.red_herb set value {item:"minecraft:nether_wart",name:"붉은 약초",type:"accessory",rarity:"common",stats:{},abilities:[{text:"",extra:[{text:"회복 구슬의 회복량이 늘어난다."}]},{text:""},{text:"",extra:[{text:"회복량 증가: "},{tk:{c:"#herbPct",x:1,d:1,p:0,u:"%"},color:"#FFE08A"}]}],desc:["쓴맛이 강할수록 잘 듣는다고들 한다."],engravings:["unyielding","berserk"]}
data modify storage rlk:items ids append value "red_herb"
