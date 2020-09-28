from userK import services as user_services
from stats.services import get_sum_score_user
from django.utils import timezone
import datetime


def create_render_data_for_tournament_week_el(request):
    user = request.user
    avatar_image = user_services.media_services.get_avatar(user)
    last_month_date_range = (timezone.now()-datetime.timedelta(days=30), timezone.now())
    month_score = get_sum_score_user(user, last_month_date_range)
    league = request.user.get_league_display()
    level = user_services.get_user_rating_lvl_dif(user.rating)
    quest_nums = [str(i).rjust(2, '0') for i in range(1, 25)]
    return {'status': 'OK',
            'level': level,
            'AvatarImage': avatar_image,
            'month_score': month_score,
            'quest_nums': quest_nums,
            'league': league}
    # else:
    #     return {'status': 'error', 'error': "This tournament doesn't exist"}


def create_render_data_for_train_el(request):
    quest_nums = [str(i).rjust(2, '0') for i in range(1, 13)]
    return {'status': 'OK',
            'quest_nums': quest_nums,
            'title': 'ТРЕНИРОВКА ЭРУДИТ-ЛОТО',
            }

