# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.lucky_coin set value {item:"minecraft:sunflower",name:"행운의 동전",type:"accessory",rarity:"common",stats:{critChance:3},abilities:[],desc:["앞면이 나오면 좋은 일이 생긴다. 뒷면은 아직 본 적이 없다."],engravings:["treasure","keen"]}
data modify storage rlk:items ids append value "lucky_coin"
