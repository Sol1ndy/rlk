# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.hourglass_shard set value {item:"minecraft:clock",name:"모래시계 조각",type:"accessory",rarity:"common",stats:{},abilities:[{text:"",extra:[{text:"원소전투 스킬의 재사용 대기 시간이 줄어든다."}]},{text:""},{text:"",extra:[{text:"재사용 대기 감소: "},{text:"5%",color:"#FFE08A"}]}],desc:["깨진 모래시계에서도 모래는 흐른다."],engravings:["cycle","emblem"]}
data modify storage rlk:items ids append value "hourglass_shard"
