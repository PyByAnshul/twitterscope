from flask import request, redirect, url_for, render_template, session, flash
from flask_admin import Admin, expose, AdminIndexView
from wtforms import Form, StringField, DateTimeField, SelectField
from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField
from markupsafe import Markup
from flask_admin.contrib.mongoengine import ModelView
from mongoengine import Document, StringField, IntField, DateTimeField, BooleanField, ListField,DictField
from globals import db
from flask_admin.actions import action
from bson import ObjectId
from threading import Thread

def init_admin(app):
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin'



    class Posts(Document):
       
        # New fields for tweet data
        post_id=StringField()
        post_link=StringField()
        content = StringField()
        content_type=StringField()
        hashtags = ListField(StringField())
        media=DictField(DictField(ListField(StringField())))
        scraped_at=DateTimeField()


    class PostsView(ModelView):
    # Column configurations
        column_list = [
            'post_link','content_type', 'content', 'hashtags','media'
        ]
        column_sortable_list = ['scraped_at']
        column_filters = ['content','content_type','post_link'
        ]
        can_export = True
        can_delete = True  # Enables bulk actions
        page_size=1000000

        # Access control
        def is_accessible(self):
            return session.get('admin_logged_in', False)

        def inaccessible_callback(self, name, **kwargs):
            flash("You must log in to access the admin panel.", "warning")
            return redirect(url_for('admin_login'))

        
    class MyAdminIndexView(AdminIndexView):
        @expose('/')
        def home(self):
            if not session.get('admin_logged_in'):
                flash("You must log in to access the admin panel.", "warning")
                return redirect(url_for('admin_login'))

            # Fetch data from MongoDB for cards
            posts_collection = db.posts
            

            total_posts = posts_collection.count_documents({})
         

            # Render template with data
            return self.render(
                'admin/admin_home.html',
                total_posts=total_posts
            )

    admin = Admin(app, name='Admin Panel', index_view=MyAdminIndexView(), template_mode='bootstrap3')
    
    admin.add_view(PostsView(Posts, 'Posts'))
    

    @app.route('/admin_login', methods=['GET', 'POST'])
    def admin_login():
        """Admin login route."""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                # Set session variable to indicate admin is logged in
                session['admin_logged_in'] = True
                flash("Login successful", "success")
                return redirect('/admin')
            else:
                flash("Invalid credentials. Please try again.", "danger")
                return render_template('admin/admin_login.html')
        return render_template('admin/admin_login.html')

    @app.route('/admin/logout')
    def admin_logout():
        """Admin logout route."""
        session.clear()
        flash("You have been logged out.", "success")
        return redirect(url_for('admin_login'))
