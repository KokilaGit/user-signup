#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

page_header = """
<!  DOCTYPE html>
<html>
<head>
    <title>User-Signup</title>
    <style type = "text/css">
        .error {
            color: blue;
            font-size: 20px;
        }
    </style>
</head>
"""
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
  return USER_RE.match(username)

USER_MA = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return USER_MA.match(email)

USER_PAWD = re.compile(r"^.{3,20}$")
def valid_passwd(passwd):
    return USER_PAWD.match(passwd)

def signup_form(username='',email='',username_error='',password_error='',verifypassWD_error='',email_error=''):
    user_form = """
    <form action = "/welcome" method = 'post'>
    <table>
        <tr>
            <td>
                <label>
                    <strong>UserName</strong>
                </label>
            </td>
            <td>
                <input  name = "username" type = "text" value = "{0}" />
            </td>
            <td class = "error"> {2} </td>

                </tr>
                <tr>
                    <td>
                        <label>
                            <strong>Password</strong>
                        </label>
                    </td>
                    <td>
                        <input type = "password"  name = "passWD" />
                    </td>
                    <td class = "error"> {3} </td>
                </tr>
                <tr>
                    <td>
                        <label>
                            <strong>VerifyPassword</strong>
                        </label>
                    </td>
                    <td>
                        <input type = "password"  name = "verifypassWD" />
                    </td>
                    <td class = "error">  {4} </td>

                        </tr>
                        <tr>
                            <td>
                                <label>
                                    <strong>E-mail(Optional)</strong>
                                </label>
                            </td>
                            <td>
                                <input type = "text" name = "email" value = "{1}"/>
                            </td>
                            <td class = "error">  {5}</td>

                                </tr>
                            </table>

                            <input type = "submit" />
                            </form>
                            """.format(username,email,username_error,password_error,verifypassWD_error,email_error)
    return user_form

class MainHandler(webapp2.RequestHandler):

    def get(self):
        header = "<h2>Signup</h2>"
        signup_page = signup_form()
        self.response.write(page_header+header+signup_page)

class WelcomeHandler(webapp2.RequestHandler):
    def post(self):
        header = "<h2>Signup</h2>"

        username = self.request.get("username")
        passWD =  self.request.get("passWD")
        verifypassWD = self.request.get("verifypassWD")
        email = self.request.get("email")

        if valid_username(username) == None:
            user_errorPage=signup_form(username, "", "Not a valid username","","","")
            self.response.write(page_header+header+user_errorPage)
            return
        if valid_passwd(passWD) == None:
            user_errorPage=signup_form(username, "", "","Not a valid Password","","")
            self.response.write(page_header+header+user_errorPage)
            return
        if (passWD != verifypassWD):
                user_errorPage=signup_form(username,"", "","", "Password doesn't match","")
                self.response.write(page_header+header+user_errorPage)
                return
        if email:
            if valid_email(email) == None:
                user_errorPage=signup_form(username,email, "", "","","Not a valid e-mail")
                self.response.write(page_header+header+user_errorPage)
                return


        self.response.write("<h2>Welcome "+username+"</h2>")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome',WelcomeHandler)
], debug=True)
