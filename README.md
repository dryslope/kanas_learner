# Kanas learner

Small program made to learn japanese kanas (katakana and hiragana).

This was originally made to work on [Termux](https://termux.dev/en/).

Kanas are randomly ordered each time you launch the program. If you ask to guess for more than 26 kanas, all 26 kanas will be present, plus some other random kanas.

There are two ways to learn:
  - "en": A random kana will appear, and you'll have to guess the equivalent syllable in english.
  - "jp": (TODO) A random syllable will appear, and some kanas will appear. You'll have to guess which kana is the equivalent.

Use with:

```
usage: main.py [-h] [-k {katakana,hiragana}] [-g {en,jp}] [-n NUMBER]

options:
  -h, --help            show this help message and exit
  -k {katakana,hiragana}, --kanas {katakana,hiragana}
                        Which kind of kana you want to learn.
  -g {en,jp}, --guess {en,jp}
                        Which language you'll write to guess.
  -n NUMBER, --number NUMBER
                        Number of kanas to guess (26 different).
```

Example:

```
./main.py --guess en --kanas hiragana --number 50
./main.py -g en -k hiragana -n 50
```

