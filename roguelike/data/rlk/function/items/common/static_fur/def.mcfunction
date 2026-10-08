# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.static_fur set value {item:"minecraft:string",name:"정전기 털뭉치",type:"accessory",rarity:"common",stats:{electroBonus:10},abilities:[],desc:["만지면 따끔하다."],engravings:["thunder","coop"]}
data modify storage rlk:items ids append value "static_fur"
