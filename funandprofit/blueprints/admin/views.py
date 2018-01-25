""" route for admin pages """
import datetime

from flask import current_app as app
from flask import (
    Blueprint,
    redirect,
    request,
    flash,
    url_for,
    render_template)
from flask_login import login_required, current_user
from sqlalchemy import text
from lib.util_spark import send_message_to_room

from funandprofit.extensions import db
from funandprofit.blueprints.admin.models import Dashboard
from funandprofit.blueprints.user.decorators import role_required
from funandprofit.blueprints.user.models import User
from funandprofit.blueprints.admin.forms import (
    SearchForm,
    BulkDeleteForm,
    UserForm,
    BulkChangeScenarioForm
)


admin = Blueprint('admin', __name__,
                  template_folder='templates', url_prefix='/admin')


@admin.before_request
@login_required
@role_required('admin')
def before_request():
    """ Protect all of the admin endpoints. """
    pass


# Dashboard -------------------------------------------------------------------
@admin.route('')
def dashboard():
    """ we don't have a need for a dashboard yet, so just re-direct to user list """
    #group_and_count_users = Dashboard.group_and_count_users()

    #return render_template('admin/page/dashboard.html',
    #                       group_and_count_users=group_and_count_users)

    return redirect(url_for('admin.users'))


# Users -----------------------------------------------------------------------
@admin.route('/users', defaults={'page': 1}, methods=['GET', 'POST'])
@admin.route('/users/page/<int:page>', methods=['GET', 'POST'])
def users(page):
    search_form = SearchForm()
    bulk_form = BulkDeleteForm()
    scenario_form = BulkChangeScenarioForm()

    sort_by = User.sort_by(request.args.get('sort', 'created_on'),
                           request.args.get('direction', 'desc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_users = User.query \
        .filter(User.search(request.args.get('q', ''))) \
        .order_by(User.role.asc(), text(order_values)) \
        .paginate(page, 50, True)

    return render_template('admin/user/index.html',
                           form=search_form, bulk_form=bulk_form,
                           users=paginated_users, scenario_form=scenario_form)


@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
def users_edit(id):
    user = User.query.get(id)
    form = UserForm(obj=user)

    if form.validate_on_submit():
        if User.is_last_admin(user,
                              request.form.get('role'),
                              request.form.get('active')):
            flash('You are the last admin, you cannot do that.', 'error')
            return redirect(url_for('admin.users'))

        form.populate_obj(user)

        ##if not user.username:
        ##    user.username = None

        user.save()

        flash('User has been saved successfully.', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/user/edit.html', form=form, user=user)


@admin.route('/users/bulk_delete', methods=['POST'])
def users_bulk_delete():
    form = BulkDeleteForm()

    if form.validate_on_submit():
        ids = User.get_bulk_action_ids(request.form.get('scope'),
                                       request.form.getlist('bulk_ids'),
                                       omit_ids=[current_user.id],
                                       query=request.args.get('q', ''))

        delete_count = User.bulk_delete(ids)

        flash('{0} user(s) were scheduled to be deleted.'.format(delete_count),
              'success')
    else:
        flash('No users were deleted, something went wrong.', 'error')

    return redirect(url_for('admin.users'))

@admin.route('/users/bulk_change/<scenario>', methods=['GET', 'POST'])
def users_bulk_change(scenario):
    """ Change all students to a new scenario"""
    change_users = User.query.all()

    for u in change_users:
        u.current_scenario = scenario
        u.needs_help = False
        u.help_time = datetime.time()
        u.finished_scenario = False
        u.scenario_time = datetime.time()
    db.session.commit()

    scenario_message = "*Scenario #" +scenario + " is locked and loaded! All user attributes have been reset!*\n"
    send_message_to_room(app.config["SPARK_BOT_ROOM_ID"], scenario_message)

    flash('All students were scheduled to be changed.', 'success')
    return redirect(url_for('admin.users'))
