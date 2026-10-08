# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.whetstone set value {item:"minecraft:flint",name:"낡은 숫돌",type:"accessory",rarity:"common",stats:{atkPct:10},abilities:[],desc:["닳고 닳았지만 아직 날은 세울 수 있다."],engravings:["keen","berserk"]}
data modify storage rlk:items ids append value "whetstone"
