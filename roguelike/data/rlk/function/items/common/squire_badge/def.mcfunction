# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.squire_badge set value {item:"minecraft:iron_nugget",name:"견습 기사의 휘장",type:"accessory",rarity:"common",stats:{energyRecharge:20},abilities:[],desc:["기사단에 들어가면 가장 먼저 받는 것."],engravings:["emblem","guard"]}
data modify storage rlk:items ids append value "squire_badge"
