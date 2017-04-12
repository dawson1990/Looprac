from werkzeug.utils import secure_filename
import os


def delete_item(email):
    try:
        basedir = os.path.abspath(os.path.dirname(__file__))
        filename = secure_filename(email + '.jpg')
        os.remove(os.path.join(basedir, 'Uploads/', filename))
    except Exception as e:
        print('Error deleting image from server:', e)
    return 'done'


def calculate_rating(star_count_data):
    # weighted average
    return (5*star_count_data['5'] + 4 * star_count_data['4'] + 3 * star_count_data['3'] + 2 * star_count_data['2'] +
            1 * star_count_data['1']) / (star_count_data['5'] + star_count_data['4'] + star_count_data['3'] +
                                         star_count_data['2']+ star_count_data['1'])


