from django.contrib.staticfiles import finders

from marathon.models import MarathonWeekOfficial
from .models import ScoreHistoryElement, MarathonWeekScoreLink
from account.models import User
from stats.models import RatingHistoryElement, MarathonWeekRatingUserLink


def get_data(id):
    instance = MarathonWeekOfficial.objects.filter(id=id)
    if instance.exists():
        instance = instance.first()
        rounds = instance.rounds.all()
        number_of_rounds = len(rounds)
        author = instance.author

        ratings_common = get_sorted_ratings_by_rounds
        return {
            'marathon': {
                'id': id,
                'num_of_rounds': number_of_rounds,
                'author': {
                    'firstname': author.firstName,
                    'lastname': author.lastName,
                    'city': author.city
                },
                'ratings': {
                    'common': ratings_common(rounds),
                    'super': ratings_common(rounds, 'super'),
                    'premier': ratings_common(rounds, 'premier'),
                    'highest': ratings_common(rounds, 'highest'),
                    'student': ratings_common(rounds, 'student'),
                    'college': ratings_common(rounds, 'college'),
                    'school': ratings_common(rounds, 'school'),
                }
            }
        }


def get_sorted_ratings_by_rounds(rounds, league=None):
    rounds_order = [f'{round.id}' for i, round in enumerate(rounds.order_by('date_time_start'))]

    def get_score_rounds(player):
        rounds_score = []
        sort_helper = {}
        for round in rounds:
            if league == 'super':
                link_instance = round.marathonweekscorelink_set.filter(score_instance__player=player)
            else:
                link_instance = round.marathonweekscorelink_set.filter(score_instance__player=player)

            if link_instance.exists():
                round_id = link_instance.first().round_instance.id
                score = link_instance.first().score_instance.value
                sort_helper[f'{round_id}'] = score
        for i in rounds_order:
            score = sort_helper.get(i, 0)
            rounds_score.append(score)
        return rounds_score

    if league:
        league = 'l6' if league == 'super' else \
            'l5' if league == 'premier' else \
                'l4' if league == 'highest' else \
                    'l3' if league == 'student' else \
                        'l2' if league == 'college' else \
                            'l1' if league == 'school' else Null
        if (marathon := rounds.first().marathonweekofficial_set.first()).is_continuous:
            players = [player for player in marathon.players.filter(league=league)]
        else:
            players = set([player for round in rounds for player in round.players.filter(league=league)])
    else:
        if (marathon := rounds.first().marathonweekofficial_set.first()).is_continuous:
            players = [player for player in marathon.players.all()]
        else:
            players = set([player for round in rounds for player in round.players.all()])

    rating_common_rows = [{
        'username': player.username,
        'hide_name': player.hide_my_name,
        'firstname': player.firstName if not player.hide_my_name else None,
        'lastname': player.lastName if not player.hide_my_name else None,
        'city': player.city if not player.hide_my_name else None,
        'score_rounds': get_score_rounds(player),
        'sum': sum(get_score_rounds(player))
    } for player in players]
    ratings = sorted(rating_common_rows, key=lambda x: x['sum'], reverse=True)
    return ratings


def write_rating(rating, round):
    for row in rating:
        player = User.objects.get(username=row['username'])
        value = row['score']
        score_instance = ScoreHistoryElement.objects.create(player=player, value=value)
        MarathonWeekScoreLink.objects.create(score_instance=score_instance, round_instance=round)


def give_rating_to_players(rounds, add_rating=100, num_positions=100):
    for i in get_sorted_ratings_by_rounds(rounds)[:num_positions]:
        username = i['username']
        user = User.objects.get(username=username)
        rating_instance = RatingHistoryElement.objects.create(player=user, value=add_rating)
        marathon_instance = rounds.first().marathonweekofficial_set.first()
        MarathonWeekRatingUserLink.objects.create(rating_instance=rating_instance, marathon_instance=marathon_instance)
        add_rating -= 1
