import datetime

from flask import Flask, g
from flask import render_template, request, flash, redirect, url_for

from flask_login import login_user, logout_user, current_user, login_required
from flask_login.mixins import AnonymousUserMixin

from app import app, db, login_manager
from app.models import Task, Status, User, Project
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def kanban():
    # if user isnt logged in redirect them to login page
    if g.user.is_anonymous:
        return redirect(url_for('login'))
    
    status_todo = Status.query.filter_by(name='todo').first()
    todo = Task.query.filter_by(status=status_todo)
    
    status_doing = Status.query.filter_by(name='doing').first()
    doing = Task.query.filter_by(status=status_doing)
    
    status_done = Status.query.filter_by(name='done').first()
    done = Task.query.filter_by(status=status_done)
    
    context = {'todo_tasks': todo,
               'doing_tasks': doing,
               'done_tasks': done}
    
    return render_template('kanban.html', **context)


@app.route('/project/<project>')
def kanban_project(project):
    # if user isnt logged in redirect them to login page
    if g.user.is_anonymous:
        return redirect(url_for('login'))
    
    status_todo = Status.query.filter_by(name='todo').first()
    todo = Task.query.filter_by(status=status_todo, project_id=project)
    
    status_doing = Status.query.filter_by(name='doing').first()
    doing = Task.query.filter_by(status=status_doing, project_id=project)
    
    status_done = Status.query.filter_by(name='done').first()
    done = Task.query.filter_by(status=status_done, project_id=project)

    context = {'todo_tasks': todo,
               'doing_tasks': doing,
               'done_tasks': done,
               'user': g.user}
    
    if project is not None:
        project = Project.query.filter_by(id=project).first()
        context['project'] = project
    
    return render_template('kanban.html', **context)


@app.route('/new_task')
@login_required
def new_task():
    return render_template('new_task.html')


@app.route('/update_status', methods=['POST', 'GET'])
@login_required
def update_status():
    '''called from JS to notify database when a task changes status'''
    try:
        req_args = request.values.to_dict()
        # get task
        task = Task.query.filter_by(id=req_args['taskid'][1:]).first()
        
        # get status
        status = Status.query.filter_by(name=req_args['statusname']).first()
        
        # set dates n shit
        if status.name == 'todo':
            task.owner = None
            task.owned_date = None
            task.completer = None
            task.complete_date = None
        elif status.name == 'doing':
            task.owner = g.user.username
            task.owned_date = datetime.datetime.utcnow()
            task.completer = None
            task.complete_date = None
        elif status.name == 'done':
            if task.owner is None:
                task.owner = g.user.username
                task.owned_date = datetime.datetime.utcnow()
            task.completer = g.user.username
            task.complete_date = datetime.datetime.utcnow()
        
        # update the status
        task.status = status
        db.session.add(task)
        db.session.commit()
        return '200'
    except:
        return '500'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect('/index')
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        user = User.query.filter_by(username=form.username.data).first()
        if user != None:
            if user.check_password(form.password.data):
                login_user(user)
                flash('Logged in successfully.')
                return redirect('/index')
            else:
                flash('Incorrect Password!')
                return redirect('/login')
        else:
            flash('Unknown User!')
            return redirect('/login')        
    return render_template('login.html', form=form)    

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)


@login_manager.user_loader
def load_user(username):
    try:
        user = User.query.filter_by(username=username).first()
        user.is_anonymous = False
        return user
    except:
        return False


@app.before_request
def before_request():
    g.user = current_user
    

@app.errorhandler(401)
def page_not_found(e):
    return render_template('401.html'), 401


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%b %d, %Y'
    return native.strftime(format)