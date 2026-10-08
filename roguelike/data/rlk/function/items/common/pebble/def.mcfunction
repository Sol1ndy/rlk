# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.pebble set value {item:"minecraft:stone_button",name:"조약돌",type:"accessory",rarity:"common",stats:{geoBonus:10},abilities:[],desc:["손에 쥐기 딱 좋은 크기."],engravings:["vajra","petra"]}
data modify storage rlk:items ids append value "pebble"
