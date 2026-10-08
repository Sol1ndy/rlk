# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.dried_fish set value {item:"minecraft:cod",name:"말린 생선",type:"accessory",rarity:"common",stats:{hpPct:10},abilities:[],desc:["오래 씹을수록 맛이 난다."],engravings:["tide","unyielding"]}
data modify storage rlk:items ids append value "dried_fish"
