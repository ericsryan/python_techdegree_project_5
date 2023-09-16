import datetime

from flask import redirect, render_template, request, url_for

from models import app, db, Project


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/projects/new', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        print("Form logic")
        new_project = Project(
            title = request.form['title'],
            date = datetime.datetime.strptime(request.form['date'], "%m/%d/%Y").date(),
            description = request.form['description'],
            skills = request.form['skills'],
            repo_link = request.form['github']
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('projectform.html')


@app.route('/projects/<id>')
def view_project(id):
    project = Project.query.get_or_404(id)
    project_skills = [skill for skill in project.skills.split(', ')]
    return render_template('detail.html', project=project, project_skills=project_skills)


@app.route('/projects/<id>/edit', methods=['GET', 'POST'])
def edit_project(id):
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        project.title = request.form['title']
        project.date = datetime.datetime.strptime(request.form['date'], "%m/%d/%Y").date()
        project.description = request.form['description']
        project.skills = request.form['skills']
        project.repo_link = request.form['github']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_projectform.html', project=project)


@app.route('/projects/<id>/delete')
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('index'))


@app.template_filter('format_date')
def format_date_filter(date_object):
    return date_object.strftime("%-m/%-d/%Y")


@app.context_processor
def inject_projects():
    projects = Project.query.all()
    return dict(projects=projects)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', msg=error), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000, host='127.0.0.1')