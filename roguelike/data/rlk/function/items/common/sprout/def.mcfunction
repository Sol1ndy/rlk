# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.sprout set value {item:"minecraft:wheat_seeds",name:"새싹",type:"accessory",rarity:"common",stats:{dendroBonus:10},abilities:[],desc:["어디에 심어도 자란다."],engravings:["erode","lunar"]}
data modify storage rlk:items ids append value "sprout"
