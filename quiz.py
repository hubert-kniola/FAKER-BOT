import random as rnd
import re

from jikanpy import AioJikan
from typing import Dict, List, Tuple
#from Levenshtein import distance
from fuzzywuzzy import fuzz


class Participant:
    ''' Zbiera ocenione głosy oddane przez uczestnika.
    '''

    def __init__(self, name: str) -> None:
        self.name = name
        self.votes: List[Tuple[str, bool]] = []

    def get_summary(self) -> Tuple[List[str], List[str]]:
        ''' Zwraca wybory gracza, 1 - poprawne, 2 - niepoprawne
        '''
        return [song for song, result in self.votes if result], [song for song, result in self.votes if not result]

    def get_points(self) -> int:
        return sum([1 if result else 0 for _song, result in self.votes])

    def __repr__(self) -> str:
        return self.name


class Entry:
    def __init__(self, anime: Dict) -> None:
        self.titles = [anime['title_english'], anime['title']]

        opening_amount = len(anime['opening_themes']) - 1
        assert opening_amount >= 0

        self.index = rnd.randint(0, len(anime['opening_themes']) - 1)
        self.element = f"OP {self.index + 1}: {anime['opening_themes'][self.index]}"

    def verify(self, vote: str, bias=5) -> bool:
        def strip(s):
            return re.sub(r' \t~`.:@#$%^&\+\*;><,\?!-√\(\)', r'', s.lower())

        vote = strip(vote)

        for title in self.titles:
            #if distance(strip(title), vote) <= bias:
            if fuzz.ratio(strip(title), vote) <= bias:
                return True

        return False

    def query(self) -> str:
        return f'{self.titles[0]} opening {self.index + 1}'

    @staticmethod
    async def random_async(pages=8):
        async with AioJikan() as jikan:
            pages = 8 if pages < 1 else pages

            page_no = rnd.randint(1, pages)
            item_no = rnd.randint(0, 49)

            page = await jikan.top('anime', page=page_no, subtype='bypopularity')
            anime = await jikan.anime(page['top'][item_no]['mal_id'])

            try:
                return Entry(anime)
            except AssertionError:
                return await Entry.random_async(pages)


class Quiz:
    def __init__(self,
                 name: str,
                 song_count: int,
                 difficulty: int) -> None:

        self.name = name
        self.songs_left = song_count
        self.round = 1
        self.difficulty = 8 if difficulty < 1 or difficulty > 100 else difficulty

        self.participants: List[Participant] = []
        self.current_votes: Dict[str, Tuple[str, bool]] = {}
        self.current_entry: Entry = None
        self.entry_history: List[Entry] = []
        self.has_started = False

    async def new_entry(self) -> None:
        self.current_entry = await Entry.random_async(self.difficulty)
        self.entry_history.append(self.current_entry)

    def add_participant(self, p: Participant) -> None:
        if not self.has_started:
            self.participants.append(p)

    def is_participant(self, name: str) -> bool:
        return any(p.name == name for p in self.participants)

    def next_round(self) -> bool:
        self.current_entry = None
        self.has_started = True

        for p in self.participants:
            try:
                p.votes.append(self.current_votes[p.name])
            except KeyError:
                pass

        self.current_votes.clear()

        self.songs_left -= 1
        self.round += 1

        if self.songs_left == 0:
            return False

        return True

    def summary(self) -> List[Participant]:
        results = map(lambda p: (p.name, p.get_points()), self.participants)

        return list(enumerate(sorted(results, key=lambda item: item[1], reverse=True), start=1))

    def __repr__(self) -> str:
        return f'{self.name} ({len(self.participants)} participants)'
