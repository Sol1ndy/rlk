# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.dew_vial set value {item:"minecraft:glass_bottle",name:"이슬 병",type:"accessory",rarity:"common",stats:{hydroBonus:10},abilities:[],desc:["새벽에만 모을 수 있다."],engravings:["tide","cycle"]}
data modify storage rlk:items ids append value "dew_vial"
