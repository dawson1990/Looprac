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


def calculateRating(starCountData):
    # weighted average
    return (5*starCountData['5'] + 4 * starCountData['4'] + 3 * starCountData['3'] + 2 * starCountData['2'] + 1 *
            starCountData['1']) / (starCountData['5'] + starCountData['4'] + starCountData['3'] + starCountData['2']
                                   + starCountData['1'])


