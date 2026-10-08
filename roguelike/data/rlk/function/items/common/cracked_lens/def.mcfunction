# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.cracked_lens set value {item:"minecraft:spyglass",name:"금 간 렌즈",type:"accessory",rarity:"common",stats:{critChance:4},abilities:[],desc:["초점은 안 맞아도 급소는 보인다."],engravings:["keen","erode"]}
data modify storage rlk:items ids append value "cracked_lens"
