""" views for student's portal """
import datetime

from flask import current_app as app

from flask import (
    Blueprint,
    redirect,
    request,
    flash,
    url_for,
    render_template,
    jsonify)
from flask_login import login_required, current_user
from sqlalchemy import text

from lib.util_spark import send_message_to_room

from funandprofit.blueprints.user.decorators import role_required
from funandprofit.blueprints.user.models import User

portal = Blueprint('portal', __name__,
                   template_folder='templates', url_prefix='/portal')

@portal.route('')
@login_required
def portal_page():
    """ view for /portal/ route """
    user = User.query.get(current_user.id)

    return render_template('portal.html', user=user)

@portal.route('/scenario')
@login_required
def portal_loadscenario():
    """
    Labs use two digits:First digit is lab #, 2nd is advanced level (0=base)
    Ex: T1A0 = Task 1, Advanced Task 0 (not an advanced task)
    BGP Lab uses Scenarios: 10-39.
    IPv6 Lab uses Scenario Range: 40-69
    """
    if current_user.current_scenario == 10:
        return render_template('scenarios/T1A0.html')
    elif current_user.current_scenario == 11:
        return render_template('scenarios/T1A1.html')
    elif current_user.current_scenario == 20:
        return render_template('scenarios/T2A0.html')
    elif current_user.current_scenario == 21:
        return render_template('scenarios/T2A1.html')
    elif current_user.current_scenario == 22:
        return render_template('scenarios/T2A2.html')
    elif current_user.current_scenario == 30:
        return render_template('scenarios/T3A0.html')
    elif current_user.current_scenario == 31:
        return render_template('scenarios/T3A1.html')
    elif current_user.current_scenario == 40:
        return render_template('scenarios/T4A0.html')
    elif current_user.current_scenario == 41:
        return render_template('scenarios/T4A1.html')
    elif current_user.current_scenario == 50:
        return render_template('scenarios/T5A0.html')
    elif current_user.current_scenario == 51:
        return render_template('scenarios/T5A1.html')
    elif current_user.current_scenario == 60:
        return render_template('scenarios/T6A0.html')
    elif current_user.current_scenario == 61:
        return render_template('scenarios/T6A1.html')
    else:
        return render_template('scenarios/nomessages.html')

@portal.route('/help', methods=['GET', 'POST'])
@login_required
def portal_help():
    """ subtract money and call proctor """
    current_user.help_time = datetime.datetime.now().time()
    current_user.needs_help = True
    current_user.money = current_user.money - 5

    current_user.save()

    room_id = app.config["SPARK_BOT_ROOM_ID"]
    message = "⁉️ **" +current_user.first_name + "** (Student#" + str(current_user.student_number) + ") ** has requested **help**!\n"
    send_message_to_room(room_id, message)

    return jsonify({'result' : 'success', 'user_money' : current_user.money})

@portal.route('/finish', methods=['GET', 'POST'])
def finish():
    """ mark this student as 'finished' and alert spark room """
    current_user.finished_scenario = True
    current_user.scenario_time = datetime.datetime.now().time()

    current_user.save()

    room_id = app.config["SPARK_BOT_ROOM_ID"]
    message = "✅  **" +current_user.first_name + "** (Student#" + str(current_user.student_number) + ") ** has signaled **finished**!\n"
    send_message_to_room(room_id, message)

    return jsonify({'result' : 'success'})

@portal.route('/supplement')
def portal_loadsupplement():
    """
    Loads supplemental material based on student's current scenario
    """
    if current_user.current_scenario == 10:
        return render_template('supplement/sup-T1.html')
    elif current_user.current_scenario == 20:
        return render_template('supplement/sup-T2.html')
    elif current_user.current_scenario == 30:
        return render_template('supplement/sup-T3.html')
    elif current_user.current_scenario == 40:
        return render_template('supplement/sup-T4.html')
    elif current_user.current_scenario == 50:
        return render_template('supplement/sup-T5.html')
    elif current_user.current_scenario == 60:
        return render_template('supplement/sup-T6.html')
    else:
        return render_template('supplement/nomessages.html')

@portal.route('/refreshmoney', methods=['GET'])
def returnmoney():
    """ route used to periodically refresh the user's money """
    return jsonify({'result' : 'success', 'user_money' : current_user.money})
