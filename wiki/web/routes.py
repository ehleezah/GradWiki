"""
    Routes
    ~~~~~~
"""
import os
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import Flask
from flask import send_from_directory
from werkzeug.utils import secure_filename

from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from wiki.core import Processor
from wiki.web.forms import EditorForm
# from wiki.web.forms import LoginForm
from wiki.web.forms import SignInForm
from wiki.web.forms import SearchForm
from wiki.web.forms import URLForm
from wiki.web.forms import CreateProfileForm
from wiki.web import current_wiki
from wiki.web import current_users
from wiki.web.user import protect
from wiki.web.profilemanager import User
from wiki.web.profilemanager import db

bp = Blueprint('wiki', __name__)

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'C:/Users/Apekshya/Desktop/Semester-4/Software Engineering/Project/wiki_flask/GradWiki/uploads'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'mp3', 'mp4', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'gif', 'pdf', 'png', 'jpg', 'jpeg', 'zip'])
#Content length that can be uploaded
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024 #1GB
# For a given file, return whether it's an allowed type or not

@bp.route('/')
@protect
def home():
    page = current_wiki.get('home')
    if page:
        "<h2> NEW USER REGISTER HERE</h2>"
        return display('home')
    return render_template('home.html')


@bp.route('/index/')
@protect
def index():
    pages = current_wiki.index()
    return render_template('index.html', pages=pages)


@bp.route('/<path:url>/')
@protect
def display(url):
    page = current_wiki.get_or_404(url)
    return render_template('page.html', page=page)


@bp.route('/create/', methods=['GET', 'POST'])
@protect
def create():
    form = URLForm()
    if form.validate_on_submit():
        return redirect(url_for(
            'wiki.edit', url=form.clean_url(form.url.data)))
    return render_template('create.html', form=form)


@bp.route('/edit/<path:url>/', methods=['GET', 'POST'])
@protect
def edit(url):
    page = current_wiki.get(url)
    form = EditorForm(obj=page)
    if form.validate_on_submit():
        if not page:
            page = current_wiki.get_bare(url)
        form.populate_obj(page)
        page.save()
        flash('"%s" was saved.' % page.title, 'success')
        return redirect(url_for('wiki.display', url=url))
    return render_template('editor.html', form=form, page=page)


@bp.route('/preview/', methods=['POST'])
@protect
def preview():
    data = {}
    processor = Processor(request.form['body'])
    data['html'], data['body'], data['meta'] = processor.process()
    return data['html']


@bp.route('/move/<path:url>/', methods=['GET', 'POST'])
@protect
def move(url):
    page = current_wiki.get_or_404(url)
    form = URLForm(obj=page)
    if form.validate_on_submit():
        newurl = form.url.data
        current_wiki.move(url, newurl)
        return redirect(url_for('wiki.display', url=newurl))
    return render_template('move.html', form=form, page=page)


@bp.route('/delete/<path:url>/')
@protect
def delete(url):
    page = current_wiki.get_or_404(url)
    current_wiki.delete(url)
    flash('Page "%s" was deleted.' % page.title, 'success')
    return redirect(url_for('wiki.home'))


@bp.route('/tags/')
@protect
def tags():
    tags = current_wiki.get_tags()
    return render_template('tags.html', tags=tags)


@bp.route('/tag/<string:name>/')
@protect
def tag(name):
    tagged = current_wiki.index_by_tag(name)
    return render_template('tag.html', pages=tagged, tag=name)


@bp.route('/search/', methods=['GET', 'POST'])
@protect
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = current_wiki.search(form.term.data, form.ignore_case.data)
        return render_template('search.html', form=form,
                               results=results, search=form.term.data)
    return render_template('search.html', form=form, search=None)


@bp.route('/createprofile/', methods=['GET', 'POST'])
def user_profile():
    form = CreateProfileForm()
    if request.method == 'POST':
        new_user = User(fullname=form.name.data, username=form.username.data, password=form.password.data,
                        email=form.email.data, phone=form.email.data, address=form.address.data)
        db.session.add(new_user)
        db.session.commit()
        flash("YOUR PROFILE IS SUCCESSFULLY CREATED")
        return redirect(url_for('wiki.user_login'))

    elif request.method == 'GET':
        return render_template("createprofile.html", form=form)


@bp.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user:
            if user.password == form.password.data:
                return redirect(request.args.get("next") or url_for('wiki.index'))
            else:
                flash("Incorrect Password")
        else:
            flash("User des not exist")
    return render_template('login.html', form=form)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Route that will process the file upload
@bp.route('/index/upload', methods=['POST'])
@protect
def upload():

        # Get the name of the uploaded files
        uploaded_files = request.files.getlist("file[]")
        filenames = []
        for file in uploaded_files:
            # Check if the file is one of the allowed types/extensions
            if file and allowed_file(file.filename):
                # Make the filename safe, remove unsupported chars
                filename = secure_filename(file.filename)
                # Move the file form the temporal folder to the upload
                # folder we setup
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # Save the filename into a list, we'll use it later
                filenames.append(filename)
        return render_template('upload.html', filenames=filenames)


# Redirect the user to the uploaded_file route, which
    # will basicaly show on the browser the uploaded file
    # Load an html page with a link to each uploaded file
#
# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@bp.route('/user/logout/')
@login_required
def user_logout():
    current_user.set('authenticated', False)
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('wiki.index'))


@bp.route('/user/')
def user_index():
    pass


@bp.route('/user/create/')
def user_create():
    pass

@bp.route('/user/<int:user_id>/')
def user_admin(user_id):
    pass


@bp.route('/user/delete/<int:user_id>/')
def user_delete(user_id):
    pass


"""
    Error Handlers
    ~~~~~~~~~~~~~~
"""


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
