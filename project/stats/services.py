def get_sym_plus_if_num_is_positive(num):
    sym = ''
    if num > 0:
        sym = '+'
    return sym


def get_sum_score_user(user):
    score_history = list(user.scorehistory_set.values('score'))

    def _get_sum(scores):
        scores_list = []
        for i in scores:
            scores_list.append(i['score'])
        return sum(scores_list)

    return _get_sum(score_history)
