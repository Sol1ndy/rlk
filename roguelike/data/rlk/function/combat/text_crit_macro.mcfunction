$summon minecraft:text_display ~$(ox) ~$(oy) ~$(oz) {billboard:"center",Tags:["dmgText"],background:0,brightness:{sky:15,block:15},shadow:true,alignment:"center",see_through:true,text:{text:"",extra:[{text:"✧",color:"$(sc1)",bold:true},{text:"✦ ",color:"$(sc2)",bold:true},{text:"$(dmg)",color:"$(col)",bold:true},{text:" ✦",color:"$(sc2)",bold:true},{text:"✧",color:"$(sc1)",bold:true}]},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.9f,1.9f,1.9f]}}
playsound minecraft:block.note_block.pling
playsound minecraft:block.note_block.bell master @a ~ ~ ~ 1 1.5
playsound minecraft:block.note_block.harp master @a ~ ~ ~ 1 1.5
