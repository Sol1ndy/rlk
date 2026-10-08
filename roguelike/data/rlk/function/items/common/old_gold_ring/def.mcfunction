# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.old_gold_ring set value {item:"minecraft:gold_nugget",name:"낡은 금반지",type:"accessory",rarity:"common",stats:{critDamage:10},abilities:[],desc:["누구의 것이었는지는 묻지 않기로 했다."],engravings:["execute","chain"]}
data modify storage rlk:items ids append value "old_gold_ring"
