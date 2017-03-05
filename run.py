from flask import Flask, render_template, request, session, redirect
# this request is different to requests, this is build in by flask!
from modles import item
from common.user import User
from common.database import Database
from common.vedio import Video

# import back-end functions from modles package
app = Flask(__name__)

# set secret key for using of session
app.secret_key = "JJT"


#  !notice! initialize the database before any requests
@app.before_first_request
def init_db():
    Database.initialize()
    # when user are not login, the database should be given a session for searching
    session['account'] = session.get('account')
    session['name'] = session.get('name')


@app.route("/")
def hello():
    return render_template("home.html")


# create login page, GET means run into the page first, POST means update data from the page
# using a array to save two methods name
@app.route("/login", methods=['GET', 'POST'])
def login_method():
    if request.method == 'POST':
        account = request.form['InputAccount']
        password = request.form['InputPassword']
        check = User.is_login_valid(account, password)
        if check is True:
            # using session package for giving response to user
            session['account'] = account
            session['name'] = User.find_user_data(account).get('name')
            # return to index page
            return redirect("/")
        else:
            message = "You account or password is wrong!"
            # using massage variable in render template function to give the message value BACK to the HTML
            return render_template("login.html", message=message)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout_method():
    # clear the session to log out user
    session['account'] = None
    return redirect("/")


@app.route("/register", methods=['GET', 'POST'])
def register_method():
    if request.method == 'POST':
        name = request.form['InputName']
        account = request.form['InputAccount']
        password = request.form['InputPassword']
        result = User.register_user(name, account, password)
        if result is True:
            # using session package for giving response to user
            session['account'] = account
            session['name'] = User.find_user_data(account).get('name')
            # return to index page
            return redirect("/")
        else:
            message = "You account is already have!"
            # using massage variable in render template function to give the message value BACK to the HTML
            return render_template("register.html", message=message)
    else:
        return render_template("register.html")


# connect to result page
@app.route("/results")
def result_page():
    url = request.url
    # only pages that are not displayed has the particular url part likes q= sp=
    page_other = request.args.get('sp')
    favorite_video = []
    # session[]: get current user info
    user_favorite = Video.find_video(session['account'])
    # user_favorite return a list with video info for a user in json format
    for video in user_favorite:
        favorite_video.append(video['link'])
    if page_other is None:
        # locate the attribute named search for particular web action, and get the value
        search = request.args.get('search')
        soup = item.find_search_content(search)
        all_pages = item.page_bar(soup)
        all_item = item.each_video(soup)
        return render_template("result.html", result=search, all_item=all_item, all_pages=all_pages, url=url,
                               favorite_video=favorite_video)
    elif page_other is not None:
        # only pages that are not displayed has the particular url part likes q= sp=
        # this search effective when you click the nav bar's numbers. It will get (x) the particular value after x=
        search = request.args.get('q')
        page_other = request.args.get('sp')
        # after adding currentpage follow the original url to trace the current page,
        # means when you click navbar at the result.html
        # and get back the value here from post-processing url, which is the FIRST page of search result
        current_page = request.args.get('currentpage')
        value = "q={}".format(search) + "&" + "sp={}".format(page_other)
        soup = item.find_page_content(value)
        all_pages = item.page_bar(soup)
        all_item = item.each_video(soup)
        # transfer those variables from Python to html pages by flask method render_template
        return render_template("result_pages.html", result=search, all_item=all_item, all_pages=all_pages,
                               current_page=current_page, int=int, url=url, favorite_video=favorite_video)
    else:
        return redirect("/")


@app.route("/favorite", methods=['GET', 'POST'])
def favorite_method():
    # session is a Flask built in variable which means it is currently login
    if session['account']:
        if request.method == 'POST':
            # currently saving the former page by store url
            # using POST get form from web pages
            url = request.form['url']
            title = request.form['title']
            link = request.form['link']
            img = request.form['img']
            account = session['account']
            # pass those variable through the python class Video
            Video(account, title, link, img).save_to_db()
            return redirect(url)
        else:
            account = session['account']
            user_videos = Video.find_video(account)
            return render_template("favorite.html", user_videos=user_videos)
    else:
        return redirect("/login")


@app.route("/delete", methods=['POST'])
def delete_method():
    link = request.form['link']
    account = session['account']
    Video.delete_video(account, link)
    return redirect("/favorite")


@app.route("/download")
def download():
    value = request.args.get('value')
    # using & to separate string into two variables
    download_type, url = value.split("&")
    if download_type == "MP3":
        item.dl_mp3(url)
        return render_template("download.html")
    elif download_type == "MP4":
        item.dl_mp4(url)
        return render_template("download.html")


if __name__ == "__main__":
    app.run(debug=False, port=4466)
