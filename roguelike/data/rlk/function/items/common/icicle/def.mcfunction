# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.icicle set value {item:"minecraft:packed_ice",name:"고드름",type:"accessory",rarity:"common",stats:{cryoBonus:10},abilities:[],desc:["눈의 나라에서는 여름에도 녹지 않는다."],engravings:["frost","chain"]}
data modify storage rlk:items ids append value "icicle"
