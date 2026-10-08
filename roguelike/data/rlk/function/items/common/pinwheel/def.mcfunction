# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.pinwheel set value {item:"minecraft:wind_charge",name:"바람개비",type:"accessory",rarity:"common",stats:{anemoBonus:10},abilities:[],desc:["바람이 없어도 가끔 혼자 돈다."],engravings:["dash","lunar"]}
data modify storage rlk:items ids append value "pinwheel"
