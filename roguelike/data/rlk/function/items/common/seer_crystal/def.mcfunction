# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.seer_crystal set value {item:"minecraft:quartz",name:"점술사의 수정 조각",type:"accessory",rarity:"common",stats:{elemMastery:40},abilities:[],desc:["들여다보면 색이 조금씩 바뀐다."],engravings:["amplify","elemental"]}
data modify storage rlk:items ids append value "seer_crystal"
