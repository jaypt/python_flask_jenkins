from flask import render_template, request, flash, redirect, url_for, jsonify
from myapp import app, JENKINS, JENKINS_PATH, TRIGGER_TYPES
from setup_details import *
from forms.all_forms import *
from jenkins.myjenkins import *
import logging

logger = logging.getLogger(__name__)


data_interface = DatabaseInterface()

def get_setup(name=None):
    data = None
    if name:
       data = data_interface.get_setup(name)
    if data:
       data = data[0]
    else:
       data = dict( TRIGGER_TYPE=None, node=None, status=None)
    return data


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    data = data_interface.get_all()
    logger.debug('displaying index page')

    form = IndexForm(request.form)
    if request.method == 'POST' and form.validate():
       return redirect(url_for('add'))

    return render_template('index.html',form=form, job=JENKINS_PATH, data=data)


#@app.route('/edit', methods=['GET'])
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    name = request.args.get('setup')
    data = get_setup(name)

    form = EditForm(request.form, **data)

    if request.method == 'POST':
       logger.debug('the data displayed on page is:'+ str(form.data))     
       if form.validate():
          logger.debug('edit form validated for:' +  str(form.data))
          data_interface.update(name, form.data)
          status, msg = update_jenkins_job(server_ip=JENKINS, new_data=form.data, old_data=data)
          if not status:
             flash('error:' + msg)
          else:
             flash('successfully updated:'+ name)
          return redirect(url_for('index')) 
       else:
          logger.debug('edit form validation failed for:'+ str(form.data))
          flash('errors with inputs:' + str(form.errors))

    return render_template('edit.html', form=form, data=data,TRIGGER_TYPES=TRIGGER_TYPES, all_status=STATUS)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    name = request.args.get('setup')
    data = get_setup(name)
    
    form = DeleteForm(request.form, **data)
    if request.method == 'POST':
       logger.debug('the delete confirmation displayed :'+ str(form.data))     
       if form.validate():
          logger.debug('delete form validated for:' + str(form.data))
          if request.form['submit'] == 'delete':
             logger.debug('deleted info:'+ str(form.data))
             data_interface.delete(name)
             status, msg = delete_jenkins_job(server_ip=JENKINS, job=name)
             if not status:
                flash('error:' + msg)
             else:
                flash('successfully deleted:'+name)
          return redirect(url_for('index')) 

    return render_template('delete.html', form=form, data=data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    data = get_setup()
    form = AddForm(request.form, ftype='add')

    if request.method == 'POST':
       logger.debug('the empty data displayed on page is:' + str(form.data))     
       if form.validate():
          logger.debug('added form validated for:'+ str(form.data))
          data_interface.add(form.data)
          status, msg = update_jenkins_job(server_ip=JENKINS, new_data=form.data)
          if not status:
             flash('error:' + msg)
          else:
             flash('successfully added:'+ form.data['TOPO_NAME'])
          return redirect(url_for('index')) 
       else:
          logger.debug('edit form validation failed for:'+ str(form.data))
          flash('errors with inputs:' + str(form.errors))

    return render_template('edit.html', form=form, data=data, TRIGGER_TYPES=TRIGGER_TYPES,all_status=STATUS )

