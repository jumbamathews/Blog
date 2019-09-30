
from flask import render_template,request,redirect,url_for,abort
from ..models import  User,Blog,Comment,Upvote,Downvote,Subscription
from . import main
from ..request import getQuotes
from flask_login import login_required, current_user
from .forms import UpdateProfile,PitchForm,CommentForm,UpvoteForm,DownvoteForm,UpdateBlogForm
from .. import db,photos
import requests 
from ..email import mail_message


# Views
@main.route('/', methods = ['GET','POST'])
def index():

    '''
    View root page function that returns the index page and its data
    '''
    posts = Blog.query.all()
    quotes = getQuotes()
    title = 'Welcome Home-Minute Pitch'
    return render_template('index.html', title = title, posts = posts,quotes=quotes)

@main.route('/blogs/new/', methods = ['GET','POST'])
@login_required
def new_blog():
    form = PitchForm()
    subscribe = Subscription.query.all()
    if form.validate_on_submit():
        title = form.title.data
        
        description = form.description.data
        user_id = current_user
        
        print(current_user._get_current_object().id)
        new_blog = Blog(user_id =current_user._get_current_object().id, title = title,description=description)
        db.session.add(new_blog)
        db.session.commit()
        for email in subscribe:
            mail_message("New Blog Alert!!!!",
                         "email/blog_alert", email.email, subscribe=subscribe)
        return redirect(url_for('main.index'))
       
    return render_template('pitches.html',form=form)



@main.route('/comment/new/<int:blog_id>', methods = ['GET','POST'])
@login_required
def new_comment(blog_id):
    form = CommentForm()
    blog=Blog.query.get(blog_id)
    if form.validate_on_submit():
        description = form.description.data

        new_comment = Comment(description = description, user_id = current_user._get_current_object().id, blog_id = blog_id)
        db.session.add(new_comment)
        db.session.commit()


        return redirect(url_for('.new_comment', blog_id= blog_id))

    all_comments = Comment.query.filter_by(blog_id = blog_id).all()
    return render_template('comments.html', form = form, comment = all_comments, blog = blog )


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    get_blogs = Blog.query.filter_by(user_id = current_user.id).all()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user ,description = get_blogs)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()
    user = current_user
    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('main.profile',uname=user.username))

    return render_template('profile/update.html',form =form,user=user)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/profile/delete/<int:blog_id>',methods = ['GET','POST'])
@login_required
def delete_blog(blog_id):
    blog=Blog.query.filter_by(id = blog_id).first()
    comments=blog.comments
    if blog.comments:
       for comment in comments:
           db.session.delete(comment)
           db.session.commit()

    user = current_user
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('.profile', uname=user.username))
    return render_template('profile/profile.html', user=user)  
@main.route('/profile/update/<int:blog_id>',methods = ['GET','POST'])
@login_required
def update_blog(blog_id):
    users = Blog.query.filter_by(id = blog_id).first()
    if users is None:
        abort(404)

    form = UpdateBlogForm()
    user = current_user
    if form.validate_on_submit():
        users.title = form.title.data
        users.description = form.description.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('main.profile',uname=user.username))

    return render_template('profile/update_blog.html',form =form,user=user)

@main.route('/blog/upvote/<int:blog_id>/upvote', methods = ['GET', 'POST'])
@login_required
def upvote(blog_id):
    blog = Blog.query.get(blog_id)
    user = current_user
    blog_upvotes = Upvote.query.filter_by(blog_id= blog_id)
    
    if Upvote.query.filter(Upvote.user_id==user.id,Upvote.blog_id==blog_id).first():
        return  redirect(url_for('main.index'))


    new_upvote = Upvote(blog_id=blog_id, user = current_user)
    new_upvote.save_upvotes()
    return redirect(url_for('main.index'))

@main.route('/blog/downvote/<int:blog_id>/downvote', methods = ['GET', 'POST'])
@login_required
def downvote(blog_id):
    blog = Blog.query.get(blog_id)
    user = current_user
    blog_downvotes = Downvote.query.filter_by(blog_id= blog_id)
    
    if Downvote.query.filter(Downvote.user_id==user.id,Downvote.blog_id==blog_id).first():
        return  redirect(url_for('main.index'))


    new_downvote = Downvote(blog_id=blog_id, user = current_user)
    new_downvote.save_downvotes()
    return redirect(url_for('main.index'))



