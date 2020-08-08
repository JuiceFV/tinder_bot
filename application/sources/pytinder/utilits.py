"""The module contains the functions which bolster
to interact with the facebook API.
Due to we need the only access token and facebook ID we use following function.
"""


import re
import requests
import robobrowser
import application.sources.pytinder.globals as globals


def get_facebook_access_token(facebook_email, facebook_password):
    """Obtain a facebook user token.
    I copied it from github, however I lost the link.

    :param facebook_email: your facebook email
    :param facebook_password: your facebook password

    :return: access token
    """
    browser = robobrowser.RoboBrowser(user_agent=globals.USER_AGENT, parser="lxml")
    browser.open(globals.FB_AUTH_LINK)
    form = browser.get_form()
    form["pass"] = facebook_password
    form["email"] = facebook_email
    browser.submit_form(form)
    form = browser.get_form()
    try:
        browser.submit_form(form, submit=form.submit_fields['__CONFIRM__'])
        access_token = re.search(
            r"access_token=([\w\d]+)", browser.response.content.decode()).groups()[0]
        return access_token
    except requests.exceptions.InvalidSchema as browserAddress:
        access_token = re.search(
            r"access_token=([\w\d]+)", str(browserAddress)).groups()[0]
        return access_token
    except Exception as ex:
        print("access token could not be retrieved. Check your username and password.")
        print("Official error: %s" % ex)
        return {"error": "access token could not be retrieved. Check your username and password."}


def get_facebook_id(access_token):
    """Get facebook id.

    :param access_token: facebook access token retrieved from get_facebook_access_token
    :return: your facebook id
    """
    if "error" in access_token:
        return {"error": "access token could not be retrieved"}
    # Gets facebook ID from access token
    request = requests.get(
        'https://graph.facebook.com/me?access_token=' + access_token)
    return request.json()["id"]