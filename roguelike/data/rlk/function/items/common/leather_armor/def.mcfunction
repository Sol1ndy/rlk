# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.leather_armor set value {item:"minecraft:leather",model:"minecraft:leather_chestplate",name:"가죽 흉갑",type:"accessory",rarity:"common",stats:{defPct:15},abilities:[],desc:["초보 모험가들이 가장 먼저 사는 물건."],engravings:["guard","unyielding"]}
data modify storage rlk:items ids append value "leather_armor"
