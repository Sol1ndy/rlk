# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.ember_matchbox set value {item:"minecraft:blaze_powder",name:"성냥갑",type:"accessory",rarity:"common",stats:{pyroBonus:10},abilities:[],desc:["젖지만 않으면 쓸 만하다."],engravings:["spirit","amplify"]}
data modify storage rlk:items ids append value "ember_matchbox"
