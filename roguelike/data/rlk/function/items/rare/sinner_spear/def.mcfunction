# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.sinner_spear set value {item:"minecraft:prismarine_shard",name:"죄인의 창끝",type:"accessory",rarity:"rare",stats:{critChance:6},abilities:[{text:"",extra:[{text:"원소폭발을 쓰면 한동안 치명타 확률이 증가한다."}]},{text:""},{text:"",extra:[{text:"치명타 확률 증가: "},{tk:{c:"#sinCrit",x:1,d:1,p:0,u:"%"},color:"#FFE08A"}]},{text:"",extra:[{text:"지속 시간: "},{tk:{c:"#sinDur",x:1,d:20,p:1,u:"초"},color:"#FFE08A"}]}],desc:["기도는 하지 않지만 일은 한다."],engravings:["keen","spirit"]}
data modify storage rlk:items ids append value "sinner_spear"
