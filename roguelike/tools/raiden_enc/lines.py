"""Raiden voice lines (typed subtitles) and the caption state. Owner: S2-SHOGUN (plan rd/plan.md E.0, D.2).
「번개여, 나의 호령을 따르라.」 (command) is now the sword switch (27); the Shogun keys of plan D.2 are appended.
"""
from .core import write

def typed(text):
    # Typewriter steps: each word grows at most two syllables at a time; punctuation
    # stays on its syllable, except the closing punctuation, which lands as the last step.
    PUNCT = '.,!?…'
    body = text.rstrip(PUNCT)
    tail = text[len(body):]
    steps, done = [], ''
    for w, word in enumerate(body.split(' ')):
        sylls = []
        for ch in word:
            if ch in PUNCT and sylls:
                sylls[-1] += ch
            else:
                sylls.append(ch)
        for k in range(0, len(sylls), 2):
            steps.append(done + ''.join(sylls[:k+2]))
        done = steps[-1] + ' '
    if tail:
        steps.append(text)
    return steps
# Boss lines from the original fight (나무위키 「마가츠 미타케 나루카미노 미코토」 3.2 패턴):
# key: (text or explicit steps, ticks per step, colour, hold of the full line)
VOICE, VOICE2 = '#d7b4ff', '#e6a3ff'
LINES = {
    'mangeop': (['그', '그 끝은', '그 끝은 만겁', '그 끝은 만겁일지니', '그 끝은 만겁일지니...'], 5, VOICE, 24),
    'eternal': ('이 몸이 곧 영원이다', 3, VOICE, 26),
    'nothing': ('그 무엇도 영원한 것은 없다.', 2, VOICE, 40),
    'eyes': ('뇌광이 영원의 땅을 비추는구나.', 2, VOICE, 24),
    'pohyeong': ('찰나의... 포영!', 3, VOICE, 22),
    'ganpa': ('간파했군.', 4, '#bfe4ff', 34),
    'noemyeong': ('뇌명.', 4, VOICE, 20),
    'will': ('뇌전은 인간의 의지 따위로 변하지 않아', 2, VOICE, 22),
    'command': ('번개여, 나의 호령을 따르라.', 2, VOICE, 22),
    'calm': ('무념 무상, 천하가 고요하리.', 2, VOICE, 12),
    'sever_one': ('무념 무상, 일도 단절.', 1, VOICE2, 16),
    'cleave_all': ('방해는 모두 베겠노라', 2, VOICE2, 22),
    'prison': ('감옥으로 만들어 주지', 2, VOICE2, 22),
    'cheonsu': ('천수의 속박!', 3, VOICE2, 30),
    'sever': ('단절!', 2, VOICE2, 20),
    'goemyeol': ('궤멸하라!', 3, VOICE2, 24),
    'pierce': ('뚫려라!', 2, VOICE2, 20),
    # S2-SHOGUN (plan D.2, wiki lines): appended, so the ids of the keys above stay.
    'too_slow': ('너무 느리군.', 3, VOICE, 20),
    'verdict': ('판결은 내려졌다.', 2, VOICE, 22),
    'return_dust': ('번개와 함께 흙으로 돌아가라.', 2, VOICE, 22),
    'shadow_world': ('속세는 그림자와 같지.', 2, VOICE, 22),
    'mock': ('가소롭군.', 3, VOICE, 22),
    'end_it': ('슬슬 끝내지.', 3, VOICE, 22),
    'absurd': ('터무니 없군.', 3, VOICE, 22),
    'musang': ('무상의 진!', 3, VOICE, 22),
    'gaze': ('이 눈으로 속세를 꿰뚫어 보리.', 2, VOICE, 24),
}
LINE_IDS = {k: i for i, k in enumerate(LINES, 1)}


def build():
    # Boss captions ride on the HUD title timer: ttlT (subtitle lifetime, view/ride_tick
    # blanks the subtitle when it runs out so the 0.5 s crosshair title cannot replay it)
    # and vBig (pauses the crosshair while a big title is up). #rdCap marks a boss caption,
    # #rdCapPat one that belongs to the running pattern and ends with it.
    write('caption/expire','''
scoreboard players set #rdCap rd 0
scoreboard players set #rdCapPat rd 0
''')
    write('caption/clear','''
scoreboard players set #rdLine rd 0
execute unless score #rdCap rd matches 1 run return 0
function rlk:boss/raiden/caption/expire
title @a[tag=player] subtitle ""
scoreboard players set @a[tag=player,scores={ttlT=1..}] ttlT 0
scoreboard players set @a[tag=player,scores={vBig=1..}] vBig 0
''')
    tick_lines = ['# Advances the boss line in progress (#rdLine id, #rdLineT age); called from tick.',
                  'execute unless score #rdLine rd matches 1.. run return 0',
                  'scoreboard players add #rdLineT rd 1']
    # One typing step = one call of the macro line/show (S2-SHOGUN: no per-step files).
    write('line/show', [
        '# One typing step of a boss line (macro: t text, c colour, s stay, f fade, n ttlT, e 1 = the last step).',
        '# One plain, quiet tick per step (same sound and pitch every time).',
        '$title @a[tag=player] times 0 $(s) $(f)',
        '$title @a[tag=player] subtitle {text:"$(t)",color:"$(c)",bold:true}',
        'execute as @a[tag=player] run function rlk:view/ttl_blank',
        '$scoreboard players set @a[tag=player] ttlT $(n)',
        'scoreboard players set #rdCap rd 1', 'scoreboard players set #rdCapPat rd 1',
        'execute as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ .3 1 0',
        '$scoreboard players set #rdSgLineEnd rd $(e)',
        'execute if score #rdSgLineEnd rd matches 1 run scoreboard players set #rdLine rd 0'])
    for key, (steps, gap, colour, hold) in LINES.items():
        steps = typed(steps) if isinstance(steps, str) else steps
        lid = LINE_IDS[key]
        write('line/'+key, [f'scoreboard players set #rdLine rd {lid}', 'scoreboard players set #rdLineT rd -1'])
        for k, text in enumerate(steps):
            last = k == len(steps)-1
            stay = hold if last else gap+6
            fade = 12 if last else 0
            assert '"' not in text and '\\' not in text, text
            args = f'{{t:"{text}",c:"{colour}",s:{stay},f:{fade},n:{stay + fade},e:{int(last)}}}'
            tick_lines.append(f'execute if score #rdLine rd matches {lid} if score #rdLineT rd matches {k*gap} run function rlk:boss/raiden/line/show {args}')
    write('line/tick', tick_lines)
    write('caption/pattern_end','''
execute if score #rdCapPat rd matches 1 run function rlk:boss/raiden/caption/clear
''')
