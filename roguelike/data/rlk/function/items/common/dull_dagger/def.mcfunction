# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.dull_dagger set value {item:"minecraft:stone_sword",name:"무딘 단검",type:"accessory",rarity:"common",stats:{atkSpeed:8},abilities:[],desc:["베는 것보다 찌르는 데 쓴다."],engravings:["flurry","execute"]}
data modify storage rlk:items ids append value "dull_dagger"
