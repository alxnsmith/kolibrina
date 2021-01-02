def get_sym_plus_if_num_is_positive(num):
    return '' if num < 0 else '+'


def get_sum_from_history(history, date_range=False):
    if date_range:
        history = history.filter(date__range=date_range)

    history = list(history.values('value'))

    def _get_sum(values):
        scores_list = [value['value'] for value in values]
        return sum(scores_list)
    return _get_sum(history)


def init_league(user):
    league = user.league
    rating = user.rating
    threshold = _get_lower_threshold(rating=rating, league=league)
    if threshold['status'] == 'SWITCH':
        user.league = threshold['new_league']
        user.save()


def _get_lower_threshold(rating, league):
    if 1000 <= rating < 3000 and (league in ['l1', 'l2']):
        return {'status': 'SWITCH', 'new_league': 'l3'}
    elif 3000 <= rating < 6000 and (league in ['l1', 'l2', 'l3']):
        return {'status': 'SWITCH', 'new_league': 'l4'}
    elif 6000 <= rating < 10000 and (league in ['l1', 'l2', 'l3', 'l4']):
        return {'status': 'SWITCH', 'new_league': 'l5'}
    elif rating >= 10000 and (league in ['l1', 'l2', 'l3', 'l5']):
        return {'status': 'SWITCH', 'new_league': 'l6'}
    else:
        return {'status': 'OK'}


class UserScore:
    def __init__(self, user_instance):
        self.user_instance = user_instance
        self.score_history_instance = self.user_instance.scorehistoryelement_set

    @property
    def score_history(self):
        return self.score_history_instance.all()

    def add(self, score):
        return self.score_history_instance.create(player=self.user_instance, value=score)

    def subtract(self, score):
        return self.score_history_instance.create(player=self.user_instance, value=-score)

    def remove_last(self):
        self.score_history_instance.last().delete()

    @staticmethod
    def remove(score_instance):
        score_instance.delete()
