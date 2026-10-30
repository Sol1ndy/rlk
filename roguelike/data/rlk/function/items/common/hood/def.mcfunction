# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.hood set value {item:"minecraft:leather",model:"minecraft:leather_helmet",name:"처형인의 두건",type:"accessory",rarity:"common",stats:{},abilities:[{text:"",extra:[{text:"체력이 절반 이하인 적에게 주는 피해가 증가한다."}]},{text:""},{text:"",extra:[{text:"적 체력 기준: "},{text:"50% 이하",color:"#FFE08A"}]},{text:"",extra:[{text:"피해 증가: "},{tk:{c:"#hoodDmg",x:1,d:1,p:0,u:"%"},color:"#FFE08A"}]}],desc:["얼굴을 가리는 건 예의다."],engravings:["execute","keen"]}
data modify storage rlk:items ids append value "hood"
