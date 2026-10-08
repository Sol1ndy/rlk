# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.chef_knife set value {item:"minecraft:pumpkin_pie",name:"주방장의 특선",type:"accessory",rarity:"epic",stats:{cryoBonus:18,hydroBonus:18},abilities:[],desc:["차가운 디저트일수록 섬세하게."],engravings:["frost","amplify"]}
data modify storage rlk:items ids append value "chef_knife"
