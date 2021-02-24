import random as rnd
import asyncio

from jikanpy import AioJikan
from enum import Enum
from typing import Dict, List, Tuple
from Levenshtein import distance


class TypeEnum(Enum):
    ''' Typ quizu:
        * STD - Każdy podaje swoją propozycję, która jest pokazywana na koniec.
        * RACE - Pierwsza osoba która się zgłosi odpowiada. Jeśli nie trafi minusowy punkt i szansa dla innych.

        Poprawność oceniana jest większościowo przez uczestników.
    '''
    STD = 1
    RACE = 2


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

    def get_points(self, qtype: TypeEnum) -> int:
        points = []

        for _song, result in self.votes:
            if result:
                points.append(1)

            elif qtype == TypeEnum.RACE:
                points.append(-1)

        return sum(points)

    def __repr__(self) -> str:
        return self.name


class Quiz:
    def __init__(self,
                 qtype: TypeEnum,
                 name: str,
                 song_count: int) -> None:

        self.qtype = qtype
        self.name = name
        self.songs_left = song_count
        self.round = 1

        self.participants: List[Participant] = []
        self.has_started = False

    def add_participant(self, p: Participant) -> None:
        if not self.has_started:
            self.participants.append(p)

    def next_round(self, votes: Dict[str, Tuple[str, bool]]) -> bool:
        self.has_started = True

        for p in self.participants:
            try:
                p.votes.append(votes[p.name])
            except KeyError:
                pass

        self.songs_left -= 1
        self.round += 1

        if self.songs_left == 0:
            return False

        return True

    def summary(self) -> List[Participant]:
        results = map(lambda p: (p.name, p.get_points(
            self.qtype)), self.participants)

        return list(enumerate(sorted(results, key=lambda item: item[1]), start=1))

    def __repr__(self) -> str:
        return f'{self.name} - {self.qtype.name}'


class Entry:
    def __init__(self, anime: Dict) -> None:
        self.titles = [anime['title_english'], anime['title']]
        self.index = rnd.randint(0, len(anime['opening_themes']) - 1)
        self.element = f"OP {self.index + 1}: {anime['opening_themes'][self.index]}"

    def verify(self, vote: str, bias=3) -> bool:
        for title in self.titles:
            if distance(title, vote) <= bias:
                return True

        return False

    def query(self) -> str:
        return f'{self.titles[0]} opening {self.index + 1}'

    @staticmethod
    async def random_async():
        async with AioJikan() as jikan:
            page_no = rnd.randint(1, 10)
            item_no = rnd.randint(0, 49)

            page = await jikan.top('anime', page=page_no, subtype='bypopularity')
            anime = await jikan.anime(page['top'][item_no]['mal_id'])

            return Entry(anime)


if __name__ == '__main__':
    async def main():
        test = await Entry.random_async()

        print(test)

    asyncio.run(main())
