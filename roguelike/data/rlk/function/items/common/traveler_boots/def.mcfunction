# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.traveler_boots set value {item:"minecraft:leather",model:"minecraft:leather_boots",name:"여행자의 장화",type:"accessory",rarity:"common",stats:{moveSpeed:8},abilities:[],desc:["밑창이 세 번 갈렸다."],engravings:["dash","cycle"]}
data modify storage rlk:items ids append value "traveler_boots"
