from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.auth import login_required
from . import mongo

bp = Blueprint('historiqueAnalyse', __name__, url_prefix='/accueil/historique')


def getHistorique(page, limit):
    skip = ((page - 1) * limit)
    analyses = list(mongo.db.historiqueAnalyse.find({}, {'_id': 0}).sort([('date', -1)]).skip(skip).limit(limit + 1))

    return analyses


# /historique
@bp.route('', methods=['GET'])
@login_required
def pageHistorique():
    # default value
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    analyses = getHistorique(page, limit)

    if len(analyses) > limit:
        has_more = True
        analyses.pop()
    else:
        has_more = False

    return render_template('analyse/historiqueAnalyse.html', analyses=analyses, page=page, limit=limit,
                           has_more=has_more)
